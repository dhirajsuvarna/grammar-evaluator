import streamlit as st
import pandas as pd
from streamlit_feedback import streamlit_feedback
from constants import Tools
from st_aggrid import AgGrid, GridOptionsBuilder

st.header("Evaluate")


@st.cache_data(experimental_allow_widgets=True)
def populate_feedback():
    print("Getting Ready...")
    df.apply(create_feedback, axis=1)


if "feedback_df" not in st.session_state:
    column_names = []
    for tool in Tools:
        column_names.append(tool.name)

    st.session_state["feedback_df"] = pd.DataFrame(columns=column_names)


@st.cache_data
def on_feedback_submit(fb, iRowIndex, iToolName):
    st.write(f"Feedback Submitted: {fb}")
    print(f"Feedback Submitted: {fb}")

    st.write(f"{iRowIndex} | {iToolName}")
    print(f"{iRowIndex} | {iToolName}")

    if fb["score"] == "👍":
        st.session_state["feedback_df"].loc[iRowIndex, iToolName] = 1
    else:
        st.session_state["feedback_df"].loc[iRowIndex, iToolName] = 0

    return


def create_feedback(iRow):
    print(f"creating feedback...{iRow.name}")
    with st.expander(f"Example {iRow.name}"):
        st.info(iRow["USER_ANSWER"])
        st.subheader(Tools.Sapling.name)
        st.write(iRow[Tools.Sapling.name], unsafe_allow_html=True)
        sapling_fb = streamlit_feedback(
            feedback_type="thumbs",
            key=f"{Tools.Sapling.name}_{iRow.name}",
            align="flex-start",
            on_submit=on_feedback_submit,
            args=(iRow.name, Tools.Sapling.name),
        )
        st.write(sapling_fb)

        st.subheader(Tools.WordTune.name)
        st.write(iRow[Tools.WordTune.name], unsafe_allow_html=True)
        wordtune_fb = streamlit_feedback(
            feedback_type="thumbs",
            key=f"{Tools.WordTune.name}_{iRow.name}",
            align="flex-start",
            on_submit=on_feedback_submit,
            args=(iRow.name, Tools.WordTune.name),
        )
        st.write(wordtune_fb)

        st.subheader(Tools.ChatGPT.name)
        st.write(iRow[Tools.ChatGPT.name], unsafe_allow_html=True)
        chatgpt_fb = streamlit_feedback(
            feedback_type="thumbs",
            key=f"{Tools.ChatGPT.name}_{iRow.name}",
            align="flex-start",
            on_submit=on_feedback_submit,
            args=(iRow.name, Tools.ChatGPT.name),
        )
        st.write(chatgpt_fb)

        st.subheader(Tools.OpenSourceLLM.name)
        st.write(iRow[Tools.OpenSourceLLM.name], unsafe_allow_html=True)
        osllm_fb = streamlit_feedback(
            feedback_type="thumbs",
            key=f"{Tools.OpenSourceLLM.name}_{iRow.name}",
            align="flex-start",
            on_submit=on_feedback_submit,
            args=(iRow.name, Tools.OpenSourceLLM.name),
        )
        st.write(osllm_fb)

        st.session_state["feedback_df"].loc[len(st.session_state["feedback_df"])] = None


if uploaded_file := st.file_uploader("Upload the File to evaluate"):
    df = pd.read_csv(uploaded_file, encoding="utf-8")
    # st.data_editor(df, disabled=True, unsafe_allow_html=True)
    table_view, feedback_view, aggrid_view = st.tabs(
        ["Table View", "Feedback View", "AG-Grid"]
    )

    with table_view:
        df_html = df.to_html(escape=False)
        st.write(df_html, unsafe_allow_html=True)

    with feedback_view:
        with st.spinner("Getting Ready..."):
            populate_feedback()

    with aggrid_view:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(wrapText=True)

        grid_response = AgGrid(
            df,
            # gridOptions=gridOptions,
            # height=grid_height,
            width="100%",
            # data_return_mode=return_mode_value,
            # update_mode=update_mode_value,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,  # Set it to True to allow jsfunction to be injected
            # enable_enterprise_modules=enable_enterprise_modules,
        )

    st.subheader("Feedback DF")
    st.dataframe(st.session_state["feedback_df"])
