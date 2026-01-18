import streamlit as st
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# --- ページ設定（サッカーアイコン） ---
st.set_page_config(page_title="熱血！英語ドリブル塾", page_icon="⚽", layout="wide")

# --- 設定（ここが心臓部です） ---
try:
    # 先生がSecretsに入れた鍵を自動で読み込みます
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
    # 最も安定している最新モデルです
    MODEL_NAME = "gemini-2.0-flash" 
except Exception as e:
    st.error(f"【設定エラー】先生、Secretsの鍵がうまく読み込めていないようです！\n{e}")
    st.stop()

# --- サッカーUIデザインの復活 ---
st.markdown("""
<style>
    .stApp { background-color: #f1f8e9; } 
    h1 { color: #1b5e20; text-align: center; font-family: 'Arial Black'; text-shadow: 2px 2px #a5d6a7; }
    .coach-bubble {
        background-color: white; border: 4px solid #4caf50;
        border-radius: 25px; padding: 25px; margin: 15px 0;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚽ 熱血！英語ドリブル塾 ⚽</h1>", unsafe_allow_html=True)

# --- 画面レイアウト ---
col1, col2 = st.columns([1, 3])
with col1:
    # コーチの画像を表示
    st.image("https://cdn-icons-png.flaticon.com/512/53/53283.png", width=150)
    st.markdown("**熱血コーチ**\n「さあ、英語のピッチへ出ようぜ！」")

with col2:
    st.write("### 🎤 コーチに話しかけるか、動詞を入力してくれ！")
    # マイク機能
    audio = mic_recorder(start_prompt="声を出す（録音開始）", stop_prompt="話し終わった（送信）", key='recorder')
    # 文字入力
    user_text = st.text_input("⌨️ 文字で入力する（例: write）")

# --- 実行処理 ---
if audio or user_text:
    with st.spinner("コーチが戦術を考えているぞ..."):
        # システムプロンプト（先生の感性）
        instruction = "あなたは熱血サッカーコーチです。英語の動詞変化をサッカーに例えて熱く解説し、最後に 3変化（例: write - wrote - written）と書いてください。"
        
        contents = [instruction]
        if audio:
            contents.append(types.Part.from_bytes(data=audio['bytes'], mime_type='audio/wav'))
        if user_text:
            contents.append(user_text)

        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=contents)
            
            # 回答を表示
            st.markdown(f'<div class="coach-bubble">{response.text}</div>', unsafe_allow_html=True)
            
            # --- ネイティブ発音機能 ---
            target_word = user_text if user_text else "Verb"
            tts = gTTS(text=target_word, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.write("🔊 **ネイティブの発音を確認だ！**")
            st.audio(fp)

        except Exception as e:
            st.error(f"コーチとの通信エラーだ！: {e}")
