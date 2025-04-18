'''
repo : https://github.com/openmarmot/smol_aws_engineer
email : andrew@openmarmot.com
notes : smolagents code_agent code
'''

from smolagents.agents import CodeAgent
from smolagents import OpenAIServerModel, DuckDuckGoSearchTool
from tools.aws_tools import get_aws_ec2_instances

import os

def load_config_file(config_path="config.txt"):
    '''Load configuration from a simple key=value text file, if it exists'''
    config = {}
    try:
        with open(config_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)  # Split on first "=" only
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        pass  # Ignore if file doesn't exist
    return config

def run_agent(query):
    '''run the code agent with the given query'''
    print('SE_API_KEY',os.getenv("SE_API_KEY"))
    #
    model = OpenAIServerModel(
    model_id=os.getenv("SE_MODEL_ID"),
    api_base=os.getenv("SE_API_BASE"),
    api_key=os.getenv("SE_API_KEY")
    )

    # note - adding the duckduckgo search tool tends to cause it to search instead of write boto3 code
    # adding the ec2_instances tool tends to cause it to use this tool in situations that don't make sense
    # it is actually better without it as long as you tell it to use 'boto3'
    #tools=[get_aws_ec2_instances]
    tools=[]
    python_imports=["boto3","json"]
    
    agent = CodeAgent(tools=tools, model=model,max_steps=10,additional_authorized_imports=python_imports)
    result=agent.run(query)

    # some additional text processing

    return result
