# smol_aws_engineer
Automating myself out of a job with HuggingFace SmolAgents

I created this repo to explore using the HuggingFace SmolAgents library to perform tasks semi-autonomously in a 
AWS Environment

![screenshot](/screenshots/smol_aws_engineer.png "Smol AWS Engineer")

### Status :
Basic functionality is in place.

I've tested it with Llama 3.1 8b running locally with llama.cpp and also with Grok2 via OpenRouter. Both models work well.
Any instruction model should work - however thinking models tend to confuse it with the thinking segments.

I've added a tool to get EC2 instance data, but in general I've found that including the tool confuses it a bit and it tends 
to overuse it. It is very prompt sensitive. Including the words "Using Boto3" will often be enough to guide it in the right 
direction. For basic commands a tool is not needed and most modern models will do quite well writing boto3 code - although 
often it takes a couple tries to get it right.  

NOTE - OBVIOUSLY USE AT YOUR OWN RISK. I HIGHLY RECOMMEND STARTING WITH A USER WITH TIGHTLY CONTROLLED READ ONLY PERMISSIONS

### Models Tested :
- Llama 3.1 8b : llama.cpp : works ok but often takes a lot of tries to get code right
- x-ai/grok-2-1212 : openrouter.ai : works great. Usually gets code right in 1-2 tries

Note on reasoning models :  
A lot of newer models have reasoning capability and include a thought section in output. This seems to be imcompatible with smolagents as of April 2025. When I try reasoning models smolagents seems to fail to retrieve code from the output.

### To use :
- Setup the AWS CLI on your system
- Associate the AWS CLI with a AWS API key for a user. To start I strongly recommend read only permissions !!
- pip install the modules in the requirements.txt
- Setup a llama.cpp server locally or get access to a openai compatible endpoint.
- copy start_server.example as start_server.sh and fill in the variables for your llm server 
- run smol_aws_engineer.py with python
- navigate to your web browser.
- Enter a query and the Smol AWS Engineer will attempt to answer it


### References
- [HuggingFace Agents course that I will totally go through at some point](https://huggingface.co/learn/agents-course/unit0/introduction)
- [HuggingFace SmolAgents Docs](https://huggingface.co/docs/smolagents/)
- [SmolAgents Github](https://github.com/huggingface/smolagents)
- [SmolAgents AI Model Leaderboard](https://huggingface.co/spaces/smolagents/smolagents-leaderboard)