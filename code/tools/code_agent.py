'''
language : Python 3.x
email : andrew@openmarmot.com
notes :
github : https://github.com/openmarmot/smol_aws_engineer
'''

from smolagents.agents import CodeAgent
from smolagents import OpenAIServerModel, DuckDuckGoSearchTool


def run_agent(query):
    '''run the code agent with the given query'''

    # setup for a local llama.cpp server
    model = OpenAIServerModel(
    model_id="none",
    api_base="http://local-inference.openmarmot.com",
    api_key="none"
    )

    agent = CodeAgent(tools=[], model=model,max_steps=10,additional_authorized_imports=["boto3","json"])
    result=agent.run(query)

    # some additional text processing

    return result
