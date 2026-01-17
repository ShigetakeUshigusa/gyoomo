import streamlit as st
import requests
import json
import io
import random
import os
api_key = st.secrets["GEMINI_API_KEY"]
from gtts import gTTS

# --- 1. アプリの設定 ---
st.set_page_config(page_title="Kashiwa English Coach", page_icon="⚽")
st.title("⚽ 柏レイソル流・英語特訓")

# 元の3行を消して、これに書き換えます
api_key = st.secrets["GEMINI_API_KEY"]

# --- 2. 数字付きファイルを見つける強力な検索機能 ---
def find_fuzzy_asset(keyword, extension):
    """
    ファイル名に「キーワード」が含まれていて、かつ「拡張子」が合っているものを探す。
    例: keyword="good", extension=".gif" 
        -> "attached_assets/good_1768626.gif" を見つけてくる！
    """
    search_dirs = ['.', 'attached_assets']

    for directory in search_dirs:
        if os.path.exists(directory):
            try:
                files = os.listdir(directory)
                for f in files:
                    # 「good」が含まれていて、かつ「.gif」で終わるなら正解！
                    if keyword.lower() in f.lower() and f.lower().endswith(extension):
                        return os.path.join(directory, f)
            except:
                continue
    return None

# --- 3. AIコーチ機能 ---
def get_coach_feedback(prompt):
    if not api_key or "ここに" in api_key: return None
    url_v1beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    for url in [url_v1beta, url_v1]:
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
        except: continue
    return None

# --- 4. 演出機能 ---
backup_quotes = ["ナイスシュート！", "素晴らしい反応だ！", "完璧なフォームだ！"]

def play_sound_fuzzy(keyword):
    # .mp3 で終わるファイルを探す
    found_path = find_fuzzy_asset(keyword, ".mp3")
    if found_path:
        st.audio(found_path, format='audio/mp3', autoplay=True)

def show_image_fuzzy(keyword):
    # .gif で終わるファイルを探す
    found_path = find_fuzzy_asset(keyword, ".gif")
    if found_path:
        st.image(found_path)

def play_tts(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp, format='audio/mp3')
    except: pass

# --- 5. ゲームデータ初期化 ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'round' not in st.session_state: st.session_state.round = 1
if 'game_state' not in st.session_state: st.session_state.game_state = 'answering' 
if 'current_verb' not in st.session_state: st.session_state.current_verb = None
if 'last_result' not in st.session_state: st.session_state.last_result = None

# 動詞リスト
verbs = [
    {"base": "write", "past": "wrote", "pp": "written", "ja": "書く"},
    {"base": "go", "past": "went", "pp": "gone", "ja": "行く"},
    {"base": "run", "past": "ran", "pp": "run", "ja": "走る"},
    {"base": "eat", "past": "ate", "pp": "eaten", "ja": "食べる"},
    {"base": "see", "past": "saw", "pp": "seen", "ja": "見る"},
    {"base": "speak", "past": "spoke", "pp": "spoken", "ja": "話す"},
    {"base": "take", "past": "took", "pp": "taken", "ja": "取る"},
    {"base": "make", "past": "made", "pp": "made", "ja": "作る"},
    {"base": "come", "past": "came", "pp": "come", "ja": "来る"},
    {"base": "know", "past": "knew", "pp": "known", "ja": "知る"},
    {"base": "give", "past": "gave", "pp": "given", "ja": "与える"},
    {"base": "get", "past": "got", "pp": "got", "ja": "得る"},
    {"base": "buy", "past": "bought", "pp": "bought", "ja": "買う"},
    {"base": "think", "past": "thought", "pp": "thought", "ja": "思う"},
    {"base": "teach", "past": "taught", "pp": "taught", "ja": "教える"},
    {"base": "catch", "past": "caught", "pp": "caught", "ja": "捕る"},
    {"base": "bring", "past": "brought", "pp": "brought", "ja": "持来る"},
    {"base": "fly", "past": "flew", "pp": "flown", "ja": "飛ぶ"},
    {"base": "swim", "past": "swam", "pp": "swum", "ja": "泳ぐ"},
    {"base": "cut", "past": "cut", "pp": "cut", "ja": "切る"}
]

# --- 6. 画面表示 ---
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("得点", f"{st.session_state.score} 点")
col2.metric("ラウンド", f"第 {st.session_state.round} 節")

if st.session_state.current_verb is None:
    st.session_state.current_verb = random.choice(verbs)
verb = st.session_state.current_verb

# === A. 結果画面 ===
if st.session_state.game_state == 'result':
    result = st.session_state.last_result

    if result == 'correct':
        st.success("⚽ GOAL!!!")

        # 1. 画像 (good か perfect を含む .gif を探す)
        img_keyword = random.choice(["good", "perfect"])
        show_image_fuzzy(img_keyword)

        # 2. 歓声 (clap か cheer を含む .mp3 を探す)
        sound_keyword = random.choice(["clap", "cheer"])
        play_sound_fuzzy(sound_keyword)

        # 3. 先生の声 (good か perfect を含む .mp3 を探す)
        # ※ここが重要：同じ "good" でも .mp3 だけを探すので画像と混ざらない！
        voice_keyword = random.choice(["good", "perfect"])
        play_sound_fuzzy(voice_keyword)

        st.balloons()
        st.markdown(f"**正解:** {verb['base']} → {verb['past']} → {verb['pp']}")

        # 4. 英語音声 (TTS)
        play_tts(f"Good job! {verb['base']}, {verb['past']}, {verb['pp']}")

        # AIコメント
        if 'feedback_text' not in st.session_state:
            p_text = f"Praise student for {verb['base']} -> {verb['past']}. Soccer style. Japanese translation."
            feedback = get_coach_feedback(p_text)
            if not feedback: feedback = random.choice(backup_quotes)
            st.session_state.feedback_text = feedback
        st.info(f"🗣️ {st.session_state.feedback_text}")

    else:
        st.error("惜しい！")
        # 失敗時 (miss を含むファイルを探す)
        show_image_fuzzy("miss")
        play_sound_fuzzy("miss")

        st.markdown(f"**正解は:** {verb['past']} / {verb['pp']}")
        play_tts(f"The answer is {verb['past']}, and {verb['pp']}")

    if st.button("次の試合へ"):
        st.session_state.game_state = 'answering'
        st.session_state.round += 1
        st.session_state.current_verb = None
        if 'feedback_text' in st.session_state: del st.session_state.feedback_text
        st.rerun()

# === B. 回答画面 ===
else:
    st.info(f"パスが来た！:  **{verb['base']}** （{verb['ja']}）")
    with st.form(key=f"game_form_{st.session_state.round}"):
        st.write("▼ 入力 (Tabで移動)")
        c1, c2 = st.columns(2)
        past_ans = c1.text_input("過去形", key="p")
        pp_ans = c2.text_input("過去分詞", key="pp")

        if st.form_submit_button("シュート！"):
            p_in = past_ans.strip().lower()
            pp_in = pp_ans.strip().lower()
            if (p_in == verb['past'] and pp_in == verb['pp']):
                st.session_state.score += 1
                st.session_state.last_result = 'correct'
            else:
                st.session_state.last_result = 'incorrect'
            st.session_state.game_state = 'result'
            st.rerun()

st.write("")
st.caption("Produced by Kashiwa Yellow Army School")
