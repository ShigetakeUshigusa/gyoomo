import streamlit as st
import google.generativeai as genai

# タイトル
st.title("黄色い軍団：動詞変化アプリ")

# 1. 金庫（Secrets）から鍵を出す
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. AIをセット（models/ は付けないのが最新の正解です）
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 入力欄
user_input = st.text_input("調べたい動詞を入力してね（例：cut）")

if user_input:
    try:
        response = model.generate_content(f"英語の動詞 '{user_input}' の現在形・過去形・過去分詞形と覚え方を教えて。")
        st.write(response.text)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
