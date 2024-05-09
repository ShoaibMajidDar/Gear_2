from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
import copy

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

def generate_recommendation_for_customer_interaction(df):
    df_preds = copy.deepcopy(df)
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df_preds, verbose=True)
    prompt_labels = """Generate a column which will be used as label to create categorized Machine Learning problem used case and suggest the best algorithms to use in solving the machine learning problem of giving personilized advice by an RM(relationship manager).
    Label Column:
    Investment Strategy Recommendation: Indicates advice related to optimizing investment strategies based on client goals, risk tolerance, and market conditions.
    Retirement Planning Advice: Indicates advice tailored to retirement planning, including retirement savings, income planning, and retirement account management.
    Estate Planning Guidance: Indicates advice focused on estate planning, including wealth transfer, wills, trusts, and estate tax strategies.
    Education Savings Recommendations: Indicates advice related to education savings planning, such as 529 plans, education savings accounts, and investment options for college savings.
    Insurance Coverage Suggestions: Indicates advice regarding insurance coverage, including life insurance, health insurance, disability insurance, and long-term care insurance.
    Tax Planning Strategies: Indicates advice on tax planning strategies, including tax-efficient investment strategies, retirement account contributions, and tax deductions.
    """
    res = agent.invoke(prompt_labels)
    return df_preds