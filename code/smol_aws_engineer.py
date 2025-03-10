'''
language : Python 3.x
email : andrew@openmarmot.com
notes :
github : https://github.com/openmarmot/smol_aws_engineer
'''

from flask import Flask, request, render_template, jsonify
import threading
import time
import schedule
from datetime import datetime

import tools.code_agent

app = Flask(__name__)

# Shared history list and lock for thread safety
history = []
lock = threading.Lock()

# Cron tasks storage: {id: {"command": str, "start_time": datetime, "interval": int (seconds), "enabled": bool}}
cron_tasks = {}
cron_id_counter = 0
cron_lock = threading.Lock()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle immediate form submission
@app.route('/submit', methods=['POST'])
def submit():
    command = request.form['command']
    thread = threading.Thread(target=ai_worker, args=(command,))
    thread.start()
    return jsonify({"status": "processing"})

# Route to handle cron submission
@app.route('/submit_cron', methods=['POST'])
def submit_cron():
    global cron_id_counter
    command = request.form['command']
    start_time_str = request.form['start_time']  # Expected format: "YYYY-MM-DD HH:MM"
    interval = int(request.form['interval'])  # Interval in seconds
    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid start time format. Use YYYY-MM-DD HH:MM"}), 400

    with cron_lock:
        cron_id = cron_id_counter
        cron_tasks[cron_id] = {
            "command": command,
            "start_time": start_time,
            "interval": interval,
            "enabled": True,
        }
        delay = (start_time - datetime.now()).total_seconds()
        if delay > 0:
            # Schedule a one-time delay job that schedules the recurring job if enabled
            schedule.every(delay).seconds.do(
                lambda: schedule.every(interval).seconds.do(ai_worker, command, cron_id).tag(f"cron_{cron_id}")
                if cron_tasks[cron_id]["enabled"] else None
            ).tag(f"delay_{cron_id}")
        else:
            # Start the recurring job immediately
            schedule.every(interval).seconds.do(ai_worker, command, cron_id).tag(f"cron_{cron_id}")
        cron_id_counter += 1
    return jsonify({"status": "scheduled", "cron_id": cron_id})

# Route to retrieve conversation history
@app.route('/history')
def get_history():
    with lock:
        history_html = "<br><br>".join([f"<pre>{msg}</pre>" for msg in history])
    return history_html

# Route to retrieve cron tasks
@app.route('/cron_tasks')
def get_cron_tasks():
    with cron_lock:
        tasks = []
        for cid, task in cron_tasks.items():
            tasks.append({
                "id": cid,
                "command": task["command"],
                "start_time": task["start_time"].strftime("%Y-%m-%d %H:%M"),
                "interval": task["interval"],
                "enabled": task["enabled"]
            })
        return jsonify(tasks)

# Route to toggle cron task status
@app.route('/toggle_cron/<int:cron_id>', methods=['POST'])
def toggle_cron(cron_id):
    with cron_lock:
        if cron_id in cron_tasks:
            cron_tasks[cron_id]["enabled"] = not cron_tasks[cron_id]["enabled"]
            return jsonify({"status": "success", "enabled": cron_tasks[cron_id]["enabled"]})
        return jsonify({"status": "error", "message": "Cron task not found"}), 404

# Route to delete cron task
@app.route('/delete_cron/<int:cron_id>', methods=['POST'])
def delete_cron(cron_id):
    with cron_lock:
        if cron_id in cron_tasks:
            schedule.clear(f"delay_{cron_id}")
            schedule.clear(f"cron_{cron_id}")
            del cron_tasks[cron_id]
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": "Cron task not found"}), 404

# AI worker function with optional cron_id
def ai_worker(command, cron_id=None):
    if cron_id is not None:
        with cron_lock:
            if cron_id not in cron_tasks or not cron_tasks[cron_id]["enabled"]:
                return  # Skip if disabled or task not found
    start_time = time.time()
    result=tools.code_agent.run_agent(command)
    end_time = time.time()
    execution_time = end_time - start_time
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    message = f"[{timestamp}]\n Received: {command}\nResult:\n{result}\nExecution time: {execution_time:.2f} seconds"
    with lock:
        history.append(message)

# Background scheduler thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Start scheduler in a background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(debug=True)