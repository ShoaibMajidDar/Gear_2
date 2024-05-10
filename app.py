import streamlit as st
import pandas as pd
from handlers.handlers import *
import time

def load_data():
    data = None
    uploaded_file = st.file_uploader("upload customer details")
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.table(data)
    return data

def call_naratives(data, selected_id):
    generate_narrative_button = st.button("generated narratives", type="primary")
    if generate_narrative_button == True:
        narratives_df = generate_narrative(data, selected_id)
        return narratives_df

def call_email(narratives_df):
    generate_email_botton=st.button("generate email for the selected customer", type="primary")
    if generate_email_botton==True:
        generated_email = generate_email(narratives_df)
        return generated_email
    
def generate_recommendations(data, selected_id):
    generate_recommendations_button=st.button("generate recommendations for the customer Interaction",type="primary")
    if generate_recommendations_button==True:
        generated_recommendations=generate_recommendation_for_customerInteraction(data, selected_id)
        single_customer = data.iloc[selected_id]
        single_customer['label'] = generated_recommendations.split(":")[1]
        
        return single_customer
    
def another_excel():
    uploaded_file1 = st.file_uploader("upload customer advisory details")
    if uploaded_file1 is not None:
        data1 = pd.read_excel(uploaded_file1)
        return data1

# def generate_recommendations_for_another_excel(data1):
#     generate_recommendations_for_another_excel_button=st.button("generate recommendations for the customer advisory details",type="primary")
#     if generate_recommendations_for_another_excel==True:
#         generated_recommendations1=generate_recommendations_for_another_excel(data1)
#         st.write(generated_recommendations1)
#         return generated_recommendations1


        

if "data" not in st.session_state:
    st.session_state.data = None
if "narratives_df" not in st.session_state:
    st.session_state.narratives_df = None
if "option" not in st.session_state:
    st.session_state.option = None
    st.session_state.selected_id=None
    st.session_state.selected_row=None

if "generated_email" not in st.session_state:
    st.session_state.generated_email = None
if "generated_recommendations" not in st.session_state:
    st.session_state.generated_recommendations =None
if "data1" not in st.session_state:
    st.session_state.data1=None
if "generate_recommendations_for_another_excel" not in st.session_state:
    st.session_state.generate_recommendations_for_another_excel=None

if st.session_state.data is None:
    st.session_state.data = load_data()

if st.session_state.data is not None:
    if st.session_state.narratives_df is None:
        st.session_state.option=st.selectbox('Select the customer for Generating narratives:', ('customer 1', 'customer 2', 'customer 3') )
        if st.session_state.option is not None:
            st.session_state.selected_id=int(st.session_state.option.split(" ")[1])-1

        with st.spinner('generating narratives...'):
            st.session_state.narratives_df = call_naratives(st.session_state.data, st.session_state.selected_id)

if st.session_state.narratives_df is not None:
    st.success('Done! Narratives Generated.')
    st.write(st.session_state.narratives_df.iloc[0][1])

if st.session_state.narratives_df is not None:
    if st.session_state.generated_email is None:
        with st.spinner('generating emails...'):
            st.session_state.generated_email= call_email(st.session_state.narratives_df)

if st.session_state.generated_email is not None:
    st.success('Done! email Generated.')
    st.write(st.session_state.generated_email.iloc[0][1])

if st.session_state.generated_email is not None:
    st.write(st.session_state.selected_row)

if st.session_state.generated_email is not None:
    if st.session_state.generated_recommendations is None:
        st.session_state.generated_recommendations=generate_recommendations(st.session_state.data, st.session_state.selected_id)

if st.session_state.generated_recommendations is not None:   
   st.table(st.session_state.generated_recommendations)
   

if st.session_state.generated_recommendations is not None:   
    if st.session_state.data1 is None:
        st.session_state.data1=another_excel()


if st.session_state.data1 is not None:
    st.table(st.session_state.data1)
# if st.session_state.data1 is not None:
#     if st.session_state.generate_recommendations1 is None:
#         st.session_state.generate_recommendations_for_another_excel=generate_recommendations_for_another_excel()



   

