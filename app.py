import streamlit as st
import google.generativeai as genai

# 1. 金庫からAPIキーを取り出し、設定する
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("黄色い軍団 : 動詞変化アプリ")

# 2. 入力欄
user_input = st.text_input("調べたい動詞を入力してね (例: write)")

if user_input:
    # 3. AIの「脳みそ」を準備（より確実な 'models/' プレフィックスを付けます）
    # これで NotFound を回避できる可能性が非常に高まります
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"英語の動詞 '{user_input}' の現在形・過去形・過去分詞形を教えて。また、覚え方のコツも短く教えて。"
        response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        # 万が一、flashがダメな場合は標準の pro で再挑戦します
        try:
            model_pro = genai.GenerativeModel('models/gemini-pro')
            response = model_pro.generate_content(prompt)
            st.write(response.text)
        except Exception as e2:
            st.error(f"GoogleのAIサーバーが応答しません。後ほどお試しください。({e2})")
