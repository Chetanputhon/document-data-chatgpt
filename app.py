import streamlit as st
from extractors import extract_text_from_file
from llm_client import ask_gpt4_for_structure
from utils import save_to_excel, parse_response_to_json

st.set_page_config(page_title="Document Data Extractor", layout="wide")

st.title("📄 Document Data Extractor (GPT-4 + Chat UI)")
st.markdown("Upload a file and ask GPT-4 to extract structured data.")

uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "xlsx", "csv", "txt", "png", "jpg", "jpeg"])
chat_history = st.session_state.get("chat_history", [])

if uploaded_file:
    file_text = extract_text_from_file(uploaded_file)
    st.session_state["file_text"] = file_text
    st.success("File processed. You can now chat with GPT-4.")

if "file_text" in st.session_state:
    with st.chat_message("user"):
        user_input = st.text_input("Ask GPT-4 to extract data:", key="chat_input")
    if user_input:
        with st.chat_message("assistant"):
            with st.spinner("GPT-4 is thinking..."):
                response = ask_gpt4_for_structure(st.session_state["file_text"], user_input)
                st.write(response)
                structured = parse_response_to_json(response)
                if structured:
                    st.success("Structured data extracted.")
                    excel_path = save_to_excel(structured)
                    with open(excel_path, "rb") as f:
                        st.download_button("📥 Download Excel", f, file_name="structured_data.xlsx")