import streamlit as st
import google.generativeai as genai

# タイトルの表示
st.title("黄色い軍団：動詞変化アプリ")

# 1. 金庫から鍵を取り出す
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. AIの「名前」を修正（models/ をつけないのが最新のルールです）
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
        st.error(f"エラーが発生しました。設定を確認してください: {e}")
