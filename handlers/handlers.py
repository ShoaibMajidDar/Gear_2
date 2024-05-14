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

def generate_narrative(df, customer_id):
    llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-0613", verbose = True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        During the recent investment portfolio review meeting with Customer, the following data was generated
        {input}. 
        Based on the info, generate a very short summary on the customer and if and how their behavior and preferences align.
        Also give in great detailed on how we can deepen client relationships, tailor services to individual needs, 
        and anticipate client needs proactively.
        """),
        ("user", "")
    ])
    chain =  prompt | llm
    df1 = pd.DataFrame()
    row = copy.deepcopy(df.iloc[1])
    row["Preference"] = row["Preference 1"]+row["Preference 2"]+row["Preference 3"]
    
    row["Behavior Patterns"] = row['Behavior Pattern 1']+row['Behavior Pattern 2']
    
    row_n = row[["Product/Service","Feedback","Preference","Behavior Patterns"]]
    
    response = chain.invoke(row_n)
    df1 = pd.DataFrame({"customer_id":str(customer_id), "narrative":response.content}, index=[0])
    return df1

def generate_email(narratives_df):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        generate an email to the customer which provides recommendations to the user as bullet points,
        given the narrative of a customer that were generated during the last interaction with the customer.
         """),
        ("user", """{narrative}""")
    ])
    chain = prompt | llm
    row = narratives_df.iloc[0]
    res = chain.invoke({"narrative": row[1]})
    email_df = pd.DataFrame({"customer_id":str(0), "email_generated":res.content}, index=[0])
    return email_df



def generate_recommendation_for_customerInteraction(df, selected_id):
    df_preds = df.iloc[selected_id]
    llm = OpenAI(temperature=0)    
    prompt = ChatPromptTemplate.from_messages([("system", """
    Generate a column, name it label, which will be used as label to create categorized Machine Learning problem used case.
    Label Column:
    Investment Strategy Recommendation: Indicates advice related to optimizing investment strategies based on client goals, risk tolerance, and market conditions.
    Retirement Planning Advice: Indicates advice tailored to retirement planning, including retirement savings, income planning, and retirement account management.
    Estate Planning Guidance: Indicates advice focused on estate planning, including wealth transfer, wills, trusts, and estate tax strategies.
    Education Savings Recommendations: Indicates advice related to education savings planning, such as 529 plans, education savings accounts, and investment options for college savings.
    Insurance Coverage Suggestions: Indicates advice regarding insurance coverage, including life insurance, health insurance, disability insurance, and long-term care insurance.
    Tax Planning Strategies: Indicates advice on tax planning strategies, including tax-efficient investment strategies, retirement account contributions, and tax deductions.
    Generate the result in the form of dictionary containing the following key:
    label: 
    """),
    ("user", """here are the details of the customer {input}""")
    ])
    chain = prompt | llm
    res = chain.invoke(df_preds)
    return res