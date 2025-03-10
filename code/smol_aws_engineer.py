'''
language : Python 3.x
email : andrew@openmarmot.com
notes :
github : https://github.com/openmarmot/smol_aws_engineer
'''


from flask import Flask, request, render_template, jsonify
import threading
import time

import tools.code_agent

app = Flask(__name__)

# Shared history list and lock for thread safety
history = []
lock = threading.Lock()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    # Start ai_worker in a separate thread
    thread = threading.Thread(target=ai_worker, args=(text,))
    thread.start()
    return jsonify({"status": "processing"})

# Route to retrieve conversation history
@app.route('/history')
def get_history():
    with lock:
        # Format history as HTML with each message in a <pre> tag
        history_html = "<br><br>".join([f"<pre>{msg}</pre>" for msg in history])
    return history_html

# AI worker function
def ai_worker(text):
    start_time = time.time()
    result=tools.code_agent.run_agent(text)
    end_time = time.time()
    execution_time = end_time - start_time
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # Create multi-line message
    message = f"[{timestamp}]\n Received: {text}\nDone!:{result}\nExecution time: {execution_time:.2f} seconds"
    with lock:
        history.append(message)  # Add to history safely

if __name__ == '__main__':
    app.run(debug=True)