import streamlit as st
import google.generativeai as genai

st.title("最終診断：使える名前を調査中")

# 1. 鍵（Secrets）をセット
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

try:
    st.write("🔍 先生のAPIキーで、今すぐ使えるモデルを一覧表示します...")
    
    # 使えるモデルの名前をすべて取得
    available_models = [m.name for m in genai.list_models()]
    st.write("✅ 利用可能な名前の一覧:")
    st.write(available_models)
    
    # 一覧の中から「gemini-1.5-flash」を探してテスト
    if 'models/gemini-1.5-flash' in available_models:
        target = 'gemini-1.5-flash'
    else:
        # もし見当たらない場合は、一覧の最初にあるものを使ってみる
        target = available_models[0].replace('models/', '')
    
    st.write(f"🚀 '{target}' という名前で接続テストを開始します...")
    model = genai.GenerativeModel(target)
    response = model.generate_content("Hi")
    st.success(f"大成功！ AIからの返事： {response.text}")

except Exception as e:
    st.error(f"❌ 調査中にエラーが出ました: {e}")
