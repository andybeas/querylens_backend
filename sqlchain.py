"""SQL CHAIN"""

import os
import openai
import pandas as pd
# from langchain.agents import create_pandas_dataframe_agent
from langchain_experimental.agents import create_pandas_dataframe_agent

from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

# df: pd.DataFrame = pd.read_csv("./Uscensus/ahs-cab2014-chhattisgarh-durg.csv")
df: pd.DataFrame = pd.read_csv("./llm_finetuning/acs_data.csv")

with open("openai_api_key.txt", "r") as f:
    API_KEY = f.read()

os.environ["OPENAI_API_KEY"] = API_KEY

class SequentialChain:
    """Class file for SQL and Dataframe"""
    
    def __init__(self, verbose: bool=True) -> None:
        self.agent = create_pandas_dataframe_agent(
        ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0, model="gpt-4"),
        df,
        verbose=verbose,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        
    def get_agent_answer(self, query: str) -> str:
        """Get answer from agent"""
        return self.agent.run(query)
