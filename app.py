import streamlit as st
import pandas as pd


def load_data():
    data = None
    uploaded_file = st.file_uploader("choose a file")
    if uploaded_file is not None:
    #     if uploaded_file.type=='xlsx,csv':
        data = pd.read_excel(uploaded_file)
        st.write(data)
    return data

def call_naratives():
    generate_narrative=st.button("generate the narative", type="primary")
    st.write(generate_narrative)
    return generate_narrative

def call_email():
    generate_email=st.button("generate the email", type="primary")
    st.write(generate_email)
    return generate_email



# def customerID_call():
#     select_id=st.text_input('enter a customer_ID')
#     return select_id

data = load_data()
if data is not None:
    generate_narrative= call_naratives()
    if generate_narrative==True:
        generate_email=call_email()



   

