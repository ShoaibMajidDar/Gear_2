import streamlit as st
import pandas as pd
from handlers.handlers import *

def load_data():
    data = None
    uploaded_file = st.file_uploader("choose a file")
    if uploaded_file is not None:
    #     if uploaded_file.type=='xlsx,csv':
        data = pd.read_excel(uploaded_file)
        st.write(data)
    return data

def call_naratives(data):
    generate_narrative_button = st.button("generate the narative", type="primary")
    if generate_narrative_button == True:
        narratives_df = generate_narrative(data)
        st.write(narratives_df.iloc[0][1])
        return narratives_df

def call_email(narratives_df):
    generate_email_botton=st.button("generate the email", type="primary")
    if generate_email_botton==True:
        generated_email = generate_email(narratives_df)
        st.write(generated_email.iloc[0][1])
        return generated_email
    
def generate_recommendations(data):
    generate_recommendations_button=st.button("generate recommendations for the customer Interaction",type="primary")
    if generate_recommendations_button==True:
        generate_recommendations=generate_recommendations(data)
        st.write(generate_recommendations[-1])
        return generate_recommendations
        

if "data" not in st.session_state:
    st.session_state.data = None
if "narratives_df" not in st.session_state:
    st.session_state.narratives_df = None
if "generated_email" not in st.session_state:
    st.session_state.generated_email = None

if "generate_recommendations" not in st.session_state:
    st.session_state.generated_recommendations =None

if st.session_state.data is None:
    st.session_state.data = load_data()

if st.session_state.data is not None:
    if st.session_state.narratives_df is None:
        st.session_state.narratives_df= call_naratives(st.session_state.data)

if st.session_state.narratives_df is not None:
    if st.session_state.generated_email is None:
        st.session_state.generated_email=call_email(st.session_state.narratives_df)

if st.session_state.generated_email is not None:
    if st.session_state.generated_recommendations is None:
        st.session_state.generated_recommendations=generate_recommendations(st.session_state.data)


   

