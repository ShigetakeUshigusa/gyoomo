import streamlit as st
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import base64

# ==========================================
# 1. ページ基本設定 (柏レイソルカラー: 黄色と黒)
# ==========================================
st.set_page_config(
    page_title="熱血！柏魂・英語ドリブル塾",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSSデザイン (日立台の熱気を再現)
# ==========================================
# 文字が見えなくならないよう、色を強制的に指定します
st.markdown("""
<style>
    /* 全体の背景色：薄い黄色（レイソルイエローのイメージ） */
    .stApp {
        background-color: #FFFDE7 !important;
    }
    
    /* メインタイトル */
    h1 {
        color: #000000 !important; /* 黒 */
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        text-shadow: 2px 2px 0px #FDD835; /* 黄色の影 */
        font-size: 3em !important;
        padding-bottom: 20px;
        border-bottom: 5px solid #000000;
    }
    
    /* サブヘッダー */
    h3 {
        color: #000000 !important;
        font-weight: bold;
    }

    /* 通常のテキストも黒くする */
    p, label, span, div {
        color: #000000 !important;
    }

    /* コーチの吹き出しスタイル */
    .coach-bubble {
        background-color: #FFFFFF;
        border: 4px solid #000000; /* 黒枠 */
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 10px 10px 0px rgba(253, 216, 53, 0.8); /* 黄色い影 */
        font-size: 1.2em;
        line-height: 1.8;
        color: #333333 !important;
    }

    /* ユーザーの吹き出し */
    .user-bubble {
        background-color: #FFF59D; /* 薄い黄色 */
        border-radius: 15px;
        padding: 15px;
        margin-left: auto;
        margin-right: 0;
        width: fit-content;
        border: 2px solid #FBC02D;
        color: #000000 !important;
    }

    /* 重要な単語の強調 */
    .highlight {
        color: #D50000 !important; /* 赤 */
        font-weight: bold;
        font-size: 1.3em;
        background-color: #FFEBEE;
        padding: 2px 5px;
        border-radius: 5px;
    }

    /* ボタンのスタイル */
    .stButton>button {
        background-color: #FDD835 !important; /* レイソルイエロー */
        color: #000000 !important;
        border: 2px solid #000000 !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    .stButton>button:hover {
        background-color: #FBC02D !important;
        border-color: #000000 !important;
    }
    
    /* 入力ボックスのスタイル */
    .stTextInput>div>div>input {
        border: 2px solid #000000 !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. Google Gemini API設定 (最新エンジン)
# ==========================================
try:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("⚠️ 先生！『GEMINI_API_KEY』が金庫(Secrets)に見当たりません！確認してください！")
        st.stop()
    
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
    
    # 先生のご希望に合わせ、最も安定して高性能な最新モデルを使用
    MODEL_NAME = "gemini-2.0-flash" 

except Exception as e:
    st.error(f"❌ システムエラー発生！審判を呼んでくれ！\n詳細: {e}")
    st.stop()

# ==========================================
# 4. タイトルとレイアウト
# ==========================================
st.markdown("<h1>⚽ 柏魂！英語ドリブル塾 ⚽</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    # 柏レイソルカラー（黄色いユニフォーム）を想起させるアイコン
    st.image("https://cdn-icons-png.flaticon.com/512/3099/3099394.png", width=200)
    st.markdown("""
    <div style="text-align: center; font-weight: bold; margin-top: 10px; background-color: #000; color: #FDD835 !important; padding: 5px;">
    熱血コーチ<br>「日立台のように熱くいこうぜ！」
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎤 コーチにパス（質問）を出してくれ！")
    st.write("マイクボタンを押して話すか、下のボックスに動詞を入力だ！")
    
    # 音声入力コンポーネント
    audio = mic_recorder(
        start_prompt="⚽ 録音開始 (KICK OFF)",
        stop_prompt="🛑 録音終了 (WHISTLE)",
        key='recorder'
    )
    
    # テキスト入力コンポーネント
    user_text = st.text_input("⌨️ キーボードでパスを出すならここだ（例: run）")

# ==========================================
# 5. 熱血コーチの人格設定 (ここが魂です)
# ==========================================
# 先生の記憶にある「柏レイソル」の要素を強く組み込みました
SYSTEM_PROMPT = """
あなたは、Jリーグ「柏レイソル」をこよなく愛する、超熱血な英語コーチです。
生徒（ユーザー）から送られてきた「英単語（主に動詞）」について、以下のルールで徹底的に解説してください。

【キャラクター設定】
1. **口調**: 松岡修造と柏レイソルの応援団長を足して2で割ったような、とにかく熱い口調。「だ・である」調。
2. **キーワード**: 「日立台」「太陽王」「VITORIA」「柏から世界へ」などの言葉を隙あらば使う。
3. **例え話**: 文法用語を使わず、すべて「サッカーのプレー」に例えること。
   - 現在形 → 基礎練習、いつものパス回し
   - 過去形 → 終わった試合、前半戦の結果
   - 過去分詞 → ゴールネットを揺らした後、試合終了後の確定した状態
4. **愛情**: 生徒を「未来のファンタジスタ」と呼び、厳しくも愛のある指導をする。

【回答フォーマット】
以下の順序で出力してください。Markdown形式を使って見やすく装飾すること。

1. **挨拶**: 「おい！いいパス（質問）が来たな！」など。
2. **3段階の変化（超重要）**: 
   大きな文字で `原形 - 過去形 - 過去分詞形` を表示。
3. **熱血解説**: 
   それぞれの形をサッカーのシチュエーションで説明。
   （例：play はピッチに立つことだ！ played はホイッスルが鳴った後のことだ！）
4. **例文シュート**: 
   柏レイソルに関連するような、熱い例文を1つ作る。（例：オルンガはゴールを決めた、など）
5. **最後の激**: 
   「さあ、ピッチに戻って練習だ！」などの熱いメッセージ。

注意: 出力はすべて日本語で行うこと（単語や例文は英語）。
"""

# ==========================================
# 6. メイン処理 (AI思考 -> 回答 -> 音声)
# ==========================================
if audio or user_text:
    
    # 入力を確定させる
    input_content = None
    if audio:
        st.toast("ナイスパス！音声をキャッチしたぞ！", icon="⚽")
        input_content = audio['bytes']
    elif user_text:
        st.toast("ナイスパス！文字を受け取ったぞ！", icon="📝")
        input_content = user_text

    if input_content:
        # 思考中の表示
        with st.spinner("コーチが作戦ボードで作戦を練っているぞ... (Thinking)"):
            try:
                # --- A. Geminiへのリクエスト作成 ---
                contents = [SYSTEM_PROMPT]
                
                if audio:
                    # 音声データを直接渡す (Gemini 2.5の真骨頂)
                    contents.append(types.Part.from_bytes(data=audio['bytes'], mime_type='audio/wav'))
                    contents.append("この音声で言っている動詞について教えてくれ！")
                else:
                    # テキストデータを渡す
                    contents.append(f"この動詞について教えてくれ： {user_text}")

                # --- B. AIからの回答生成 ---
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents
                )
                
                # --- C. 回答の表示 (吹き出し) ---
                st.markdown(f'<div class="coach-bubble">{response.text}</div>', unsafe_allow_html=True)
                
                # --- D. ネイティブ発音の生成 (gTTS) ---
                # 解説文の中から英単語だけを抽出するのは難しいため、
                # ユーザーが入力した単語（または音声から推測される単語）の発音を作ります。
                
                # 音声入力の場合は、AIに「何の単語だったか」を聞き出す処理を省略するため、
                # 簡易的に「Listen to the pronunciation」と言わせるか、
                # テキスト入力がある場合のみその単語を読み上げます。
                
                word_to_speak = "Practice makes perfect!" # デフォルト
                if user_text:
                    word_to_speak = user_text
                
                # 音声合成
                tts = gTTS(text=word_to_speak, lang='en')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                
                st.write("---")
                st.markdown("### 🔊 ネイティブのキック（発音）を確認しろ！")
                st.audio(audio_fp, format='audio/mp3')

            except Exception as e:
                st.error(f"レッドカード！システム退場！エラーが出たぞ！\n{e}")

# ==========================================
# 7. フッター
# ==========================================
st.write("---")
st.markdown("""
<div style="text-align: center; color: #555;">
    Powered by <b>Gemini 2.5 Flash</b> | 柏魂 English Academy <br>
    Copyright © 2026 Yellow Corps. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
