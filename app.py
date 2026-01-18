import streamlit as st
from google import genai

st.title("英語動詞変化アプリ（最新版）")

# 1. 金庫（Secrets）から鍵を取り出す
API_KEY = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# 2. 最新の脳みそを指定（2.5-flash）
MODEL_NAME = "gemini-2.5-flash"

# 3. 入力欄
verb = st.text_input("英語の動詞を入力してください（例: cut）")

if verb:
    try:
        prompt = f"英語の動詞 '{verb}' の現在形・過去形・過去分詞形と覚え方を、日本語の箇条書きで教えて。"
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        st.write(response.text)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
