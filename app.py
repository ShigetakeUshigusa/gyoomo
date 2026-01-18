import streamlit as st
import google.generativeai as genai

# タイトルの表示
st.title("英語動詞変化検索アプリ")

# 1. Secrets（金庫）から鍵を取り出す
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. 最新の脳みそ（Gemini 1.5 Flash）をセット
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 入力欄
user_input = st.text_input("調べたい動詞を入力してね（例：write）")

if user_input:
    try:
        # AIに質問する
        prompt = f"英語の動詞 '{user_input}' の現在形・過去形・過去分詞形を教えて。また、覚え方のコツも短く教えて。"
        response = model.generate_content(prompt)
        
        # 結果を表示する
        st.write(response.text)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
