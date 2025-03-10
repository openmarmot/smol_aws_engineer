# smol_aws_engineer
Automating myself out of a job with HuggingFace SmolAgents

I created this repo to explore using the HuggingFace SmolAgents library to perform tasks semi-autonomously in a 
AWS Environment

![screenshot](/screenshots/smol_aws_engineer.png "Smol AWS Engineer")

### Status :
Just getting started.

So far no tools have been added but the agent can use Python and Boto3 to access your AWS environment if 
you have the AWS ClI credentials setup on your system.

It is pretty good at writing AWS code (depending on the model you use), so.. beware the consequences of what you ask.

NOTE - OBVIOUSLY USE AT YOUR OWN RISK. I HIGHLY RECOMMEND STARTING WITH A USER WITH TIGHTLY CONTROLLED READ ONLY PERMISSIONS

### To use :
- Setup the AWS CLI on your system
- Associate the AWS CLI with a AWS API key for a user. To start I strongly recommend read only permissions !!
- pip install the modules in the requirements.txt
- Setup a llama.cpp server locally (update the URL in code_agent.py). 
- run smol_aws_engineer.py with python
- navigate to your web browser.
- Enter a query and the Smol AWS Engineer will attempt to answer it


### References
- [HuggingFace Agents course that I will totally go through at some point](https://huggingface.co/learn/agents-course/unit0/introduction)
- [HuggingFace SmolAgents Docs](https://huggingface.co/docs/smolagents/)
- [SmolAgents Github](https://github.com/huggingface/smolagents)
- [SmolAgents AI Model Leaderboard](https://huggingface.co/spaces/smolagents/smolagents-leaderboard)