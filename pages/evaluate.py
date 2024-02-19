import streamlit as st
import pandas as pd

"""
todo: 
1. do not allow to sort the columns 
2. add user feedback to each row 
3. record the user feedback to sqllite database 
"""

st.header("Evaluate")

if uploaded_file := st.file_uploader("Upload the File to evaluate"):
    df = pd.read_csv(uploaded_file, encoding="utf-8")
    # st.data_editor(
    #     df,
    #     disabled=True,
    # )
    df_html = df.to_html(escape=False)
    st.write(df_html, unsafe_allow_html=True)
