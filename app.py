import streamlit as st
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# --- 1. ページ設定（サッカーアイコン） ---
st.set_page_config(page_title="熱血！英語ドリブル塾", page_icon="⚽", layout="wide")

# --- 2. 鍵の確認（ログのエラー対策） ---
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ StreamlitのSecretsに 'GEMINI_API_KEY' が設定されていません！")
        st.stop()
    
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
    MODEL_NAME = "gemini-2.0-flash" # 最新・最速の安定版
except Exception as e:
    st.error(f"初期設定エラー: {e}")
    st.stop()

# --- 3. 以前の熱いUI（サッカーデザイン）の復活 ---
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

# --- 4. 以前の「キャラクター画像」とコーチの挨拶 ---
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/53/53283.png", width=150)
    st.markdown("**熱血コーチ**\n「さあ、英語のピッチへ出ようぜ！」")

with col2:
    # --- 5. 入力エリア（音声 ＆ 文字） ---
    st.write("### 🎤 コーチに話しかけるか、動詞を入力してくれ！")
    audio = mic_recorder(start_prompt="声を出す（録音開始）", stop_prompt="話し終わった（送信）", key='recorder')
    user_text = st.text_input("⌨️ 文字で入力する（例: write）")

# --- 6. AIの熱血回答 ＆ ネイティブ発音生成 ---
if audio or user_text:
    with st.spinner("コーチが戦術（回答）を練っているぞ..."):
        # 先生の感性を吹き込んだシステムプロンプト
        instruction = """あなたは熱血サッカーコーチです。
        生徒が入力した動詞の「現在形・過去形・過去分詞形」をサッカーに例えて熱く解説してください。
        回答の最後に、その3変化だけを英語で一行（例: write - wrote - written）と書いてください。"""
        
        contents = [instruction]
        if audio:
            contents.append(types.Part.from_bytes(data=audio['bytes'], mime_type='audio/wav'))
        if user_text:
            contents.append(user_text)

        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=contents)
            
            # 吹き出しで表示
            st.markdown(f'<div class="coach-bubble">{response.text}</div>', unsafe_allow_html=True)
            
            # --- 7. ネイティブ発音（TTS）の復活！ ---
            # AIの回答から動詞の3変化部分を探して音声にする
            words = user_text if user_text else "Verb conjugation"
            tts = gTTS(text=words, lang='en') # ここでネイティブの発音を生成
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.write("🔊 **ネイティブの発音を確認だ！**")
            st.audio(fp)

        except Exception as e:
            st.error(f"コーチとの通信エラーだ！: {e}")

st.write("---")
st.caption("先生の情熱をAIで再現中。")
