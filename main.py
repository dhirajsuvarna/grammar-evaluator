import streamlit as st
import pandas as pd
import re
import logging
import sys

from logging import FileHandler, StreamHandler

# from enum import Enum

# from sapling_api import sapling_check
# from ai21_api import ai21_check
# from openai_api import openai_check
# from opensource_api import opensourcellm_check

from grammar_checker import grammar_checker

from constants import Tools


st.set_page_config(page_title="Grammar Check on Sentences", layout="wide")
st.title("Grammar Check on Sentences")


"""
set up logging 
"""

logging.basicConfig(
    handlers=[
        StreamHandler(stream=sys.stdout),
        FileHandler(filename="streamlit.log", mode="a", encoding="utf-8"),
    ],
    level=logging.INFO,
    format="{asctime} | {filename} | {levelname} | {message}",
    datefmt="%d-%m-%Y %H:%M:%S",
    style="{",
)

# logger = logging.getLogger("main_logger")
# formatter = logging.Formatter(
#     fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
# )
# fileHandler = FileHandler(filename="dhiraj.log", mode="w", encoding="utf-8")
# fileHandler.setFormatter(formatter)
# fileHandler.setLevel(logging.INFO)
# logger.addHandler(fileHandler)

# streamHandler = StreamHandler(stream=sys.stdout)
# streamHandler.setFormatter(formatter)
# streamHandler.setLevel(logging.INFO)
# logger.addHandler(streamHandler)


"""
todo:
1. add the OpenSource LLM 
2. run in batch mode
"""

default_text = "It is is more fun to talk with someone who doesnt use long, difikolt words but rather short, easy words like, What about lunch"


def clear_outputs():
    for tool in Tools:
        st.session_state[tool.name] = ""


def remove_html_tags(iText):
    return re.sub("<[^<]+?>", "", iText)


if len(st.session_state) == 0:
    for tool in Tools:
        st.session_state[tool.name] = ""

    columns = ["Text"]
    columns.extend([x.name for x in Tools])
    st.session_state["df"] = pd.DataFrame(columns=columns)

input_text = st.text_area("Insert the statement here...", value=default_text)

col_list = st.columns(len(Tools))

with col_list[0]:
    st.subheader(Tools.Sapling.name)
    if st.button("Check", key="sapling_btn"):
        # st.session_state[Tools.Sapling.name] = sapling_check(
        #     st.secrets.SAPLING_API_KEY, input_text
        # )
        st.session_state[Tools.Sapling.name] = grammar_checker(
            Tools.Sapling, input_text
        )

    st.markdown(st.session_state[Tools.Sapling.name], unsafe_allow_html=True)

with col_list[1]:
    st.subheader(Tools.WordTune.name)
    if st.button("Check", key="wordtune_btn"):
        # st.session_state[Tools.WordTune.name] = ai21_check(
        #     st.secrets.AI21_API_KEY, input_text
        # )
        st.session_state[Tools.WordTune.name] = grammar_checker(
            Tools.WordTune, input_text
        )
    st.markdown(st.session_state[Tools.WordTune.name], unsafe_allow_html=True)


with col_list[2]:
    st.subheader(Tools.ChatGPT.name)
    # cost = 0
    if st.button("Check", key="chatgpt_btn"):
        # perform the api call
        # st.session_state[Tools.ChatGPT.name] = openai_check(
        #     st.secrets.OPENAI_API_KEY, input_text
        # )
        st.session_state[Tools.ChatGPT.name] = grammar_checker(
            Tools.ChatGPT, input_text
        )
    st.markdown(st.session_state[Tools.ChatGPT.name], unsafe_allow_html=True)
    # if cost:
    #     st.metric("Cost", f"{cost} $")


with col_list[3]:
    st.subheader(Tools.OpenSourceLLM.name)
    # cost = 0
    if st.button("Check", key="openllm_btn"):
        # perform the api call
        # st.session_state[Tools.OpenSourceLLM.name] = opensourcellm_check(
        #     st.secrets.OPENROUTER_API_KEY, input_text
        # )
        st.session_state[Tools.OpenSourceLLM.name] = grammar_checker(
            Tools.OpenSourceLLM, input_text
        )

    st.markdown(st.session_state[Tools.OpenSourceLLM.name], unsafe_allow_html=True)
    # if cost:
    #     st.metric("Cost", f"{cost} $")

st.divider()

col1, col2 = st.columns(2)
if col1.button("Record", use_container_width=True):
    row = [input_text]
    for tool in Tools:
        row.append(remove_html_tags(st.session_state[tool.name]))

    df = st.session_state["df"]
    df.loc[len(df) + 1] = row

    clear_outputs()

if col2.button("Clear", use_container_width=True):
    clear_outputs()

st.write(f"### Records:")
st.data_editor(st.session_state["df"], use_container_width=True)
