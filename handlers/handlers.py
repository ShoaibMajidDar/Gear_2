from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
 
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def generate_narrative(df):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", verbose = True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Can you generate LLM narratives to identify opportunities to deepen client relationships, tailor services to individual needs, and anticipate client needs proactively. The narratives must analyze customer interactions, preferences, and behavior patterns to provide personalized recommendations and anticipate future requirements effectively."""),
        ("user", "{input}")
    ])
    chain =  prompt | llm
    df1 = pd.DataFrame()
    for i,row in df.iterrows():
        response = chain.invoke(row)
        df1 = pd.concat([df1,pd.DataFrame({"customer_id":str(i+1), "narrative":response.content}, index=[i])])
    return df1


def generate_email(narratives_df):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", " Generate an emails for Customer based on above narratives to provide recommendations as bullet points."),
        ("user", "{input}")
    ])
    chain = prompt | llm
    email_df = pd.DataFrame()
    for i,row in narratives_df.iterrows():
        res = chain.invoke({"input": row[1]})
        email_df = pd.concat([email_df,pd.DataFrame({"customer_id":str(i+1), "email_generated":res.content}, index=[i])])
    return email_df