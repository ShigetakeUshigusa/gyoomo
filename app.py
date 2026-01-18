import streamlit as st
import google.generativeai as genai

# Configure the API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize the latest Gemini 1.5 Flash model (note: no 'models/' prefix needed)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.title("英語動詞変化アプリ")

verb = st.text_input("英語の動詞を入力してください（例: go）")

if verb:
    prompt = f"Provide the conjugations for the English verb '{verb}', including base form, past tense, past participle, present participle, and third person singular. Format as a bullet list."
    with st.spinner("生成中..."):
        response = model.generate_content(prompt)
    st.markdown(response.text)
