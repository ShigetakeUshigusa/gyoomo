import streamlit as st
import google.generativeai as genai

# 1. 先生が設定した「金庫（Secrets）」からAPIキーを取り出す
api_key = st.secrets["GEMINI_API_KEY"]

# 2. AI（Gemini）の設定をする
genai.configure(api_key=api_key)
api_key = st.secrets["GEMINI_API_KEY"]

st.title("黄色い軍団：動詞変化アプリ")

# 3. 入力欄を作る
user_input = st.text_input("調べたい動詞を入力してね（例：write）")

if user_input:
    # 4. AIに質問を投げる
    prompt = f"英語の動詞 '{user_input}' の現在形・過去形・過去分詞形を教えて。また、覚え方のコツも短く教えて。"
    response = model.generate_content(prompt)
    
    # 5. AIの答えを表示する
    st.write(response.text)
