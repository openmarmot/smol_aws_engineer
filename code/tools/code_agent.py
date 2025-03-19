'''
repo : https://github.com/openmarmot/smol_aws_engineer
email : andrew@openmarmot.com
notes : smolagents code_agent code
'''

from smolagents.agents import CodeAgent
from smolagents import OpenAIServerModel, DuckDuckGoSearchTool
from tools.aws_tools import get_aws_ec2_instances


def run_agent(query):
    '''run the code agent with the given query'''

    # setup for a local llama.cpp server
    model = OpenAIServerModel(
    model_id="none",
    api_base="http://local-inference.openmarmot.com",
    api_key="none"
    )

    # note - adding the duckduckgo search tool tends to cause it to search instead of write boto3 code
    tools=[get_aws_ec2_instances]
    python_imports=["boto3","json"]
    
    agent = CodeAgent(tools=tools, model=model,max_steps=10,additional_authorized_imports=python_imports)
    result=agent.run(query)

    # some additional text processing

    return result
