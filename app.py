import streamlit as st
import google.generativeai as genai

# 金庫から鍵を取り出す
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.write("✅ 金庫の鍵は正しく読み込めました。")
    
    # 挨拶だけしてみる
    response = model.generate_content("Hello")
    st.write("✅ AIからの返答:", response.text)

except Exception as e:
    # ここで「本当の犯人」を画面に詳しく表示させます
    st.error(f"❌ 失敗の原因: {e}")
    st.write("エラーの詳細型:", type(e).__name__)
