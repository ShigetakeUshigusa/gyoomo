import streamlit as st
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder

# --- ページ設定 ---
st.set_page_config(page_title="熱血！英語ドリブル塾", page_icon="⚽", layout="wide")

# --- 設定 ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
    # ChatGPTのアドバイス通り、安定した2.5モデルを使用
    MODEL_NAME = "gemini-2.5-flash"
except Exception as e:
    st.error(f"鍵の設定を確認してください！\nエラー: {e}")
    st.stop()

# --- サッカー場のUIデザイン ---
st.markdown("""
<style>
    .stApp { background-color: #f1f8e9; } 
    h1 { color: #2e7d32; text-align: center; font-family: 'Arial Black'; }
    .coach-bubble {
        background-color: white; border: 4px solid #4caf50;
        border-radius: 25px; padding: 25px; margin: 15px 0;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚽ 熱血！英語ドリブル塾 ⚽</h1>", unsafe_allow_html=True)

# --- 入力エリア ---
st.write("### 🎤 コーチに直接話しかけるか、文字で入力してくれ！")
# マイクボタンの設置
audio = mic_recorder(start_prompt="声を出す（録音開始）", stop_prompt="話し終わった（送信）", key='recorder')
user_text = st.text_input("⌨️ 文字で入力する場合はここだ（例: write）")

# --- AIとの対話 ---
if audio or user_text:
    with st.spinner("コーチが戦術（回答）を練っているぞ..."):
        # 熱血コーチの人格を定義
        system_instruction = "あなたは熱血サッカーコーチです。英語の動詞変化を、サッカーの例え話を交えて、生徒を励ましながら熱く解説してください。"
        
        contents = [system_instruction]
        
        # 音声データをそのままGeminiに聴かせる
        if audio:
            contents.append(types.Part.from_bytes(data=audio['bytes'], mime_type='audio/wav'))
        
        # 文字入力もあれば追加
        if user_text:
            contents.append(user_text)

        try:
            # Gemini 2.5の最新エンジンで実行
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents
            )
            
            # 結果を吹き出しで表示
            st.markdown(f'<div class="coach-bubble">{response.text}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"エラーが発生したようだ！: {e}")

st.image("https://cdn-icons-png.flaticon.com/512/53/53283.png", width=100)
