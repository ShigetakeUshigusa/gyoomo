import streamlit as st
import google.generativeai as genai

# 1. APIキーの設定（金庫から取り出す）
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("黄色い軍団：動詞変化アプリ")

# 2. AIの「脳みそ」を指定（もっとも標準的な名前に固定します）
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 入力欄
user_input = st.text_input("調べたい動詞を入力してね（例：cut）")

if user_input:
    try:
        # AIに答えを聞く
        response = model.generate_content(f"英語の動詞 '{user_input}' の現在形・過去形・過去分詞形を教えて。")
        st.write(response.text)
    except Exception as e:
        # 万が一エラーが出た場合は、その内容をそのまま表示
        st.error(f"Google AIとの通信でエラーが出ました: {e}")
