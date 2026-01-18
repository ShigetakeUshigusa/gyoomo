import streamlit as st
import requests
import json
import io
import random
import os
import time
from gtts import gTTS

# --- 1. アプリの設定 ---
st.set_page_config(page_title="Kashiwa English Coach", page_icon="⚽")
st.title("⚽ 柏レイソル流・英語特訓")

# ==========================================
# ★修正点: 先生が見つけたコードの唯一の変更点です
# 金庫(Secrets)から鍵を取り出す設定にしました。これ以外は元のままです。
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secretsに GEMINI_API_KEY が設定されていません。")
    st.stop()
# ==========================================

# --- 2. 資産検索機能（数字付きファイル対応） ---
def find_fuzzy_asset(keyword, extension):
    search_dirs = ['.', 'attached_assets']
    for directory in search_dirs:
        if os.path.exists(directory):
            try:
                files = os.listdir(directory)
                for f in files:
                    if keyword.lower() in f.lower() and f.lower().endswith(extension):
                        return os.path.join(directory, f)
            except: continue
    return None

# --- 3. AIコーチ機能 ---
def get_coach_feedback(prompt):
    if not api_key: return None
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
    found_path = find_fuzzy_asset(keyword, ".mp3")
    if found_path: st.audio(found_path, format='audio/mp3', autoplay=True)

def show_image_fuzzy(keyword):
    found_path = find_fuzzy_asset(keyword, ".gif")
    if found_path: st.image(found_path)

def play_tts(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp, format='audio/mp3')
    except: pass

# --- 5. ゲームデータ初期化 ---
if 'score' not in st.session_state: st.session_state.score = 0
if 'misses' not in st.session_state: st.session_state.misses = 0 # ミス数
if 'round' not in st.session_state: st.session_state.round = 1
if 'game_state' not in st.session_state: st.session_state.game_state = 'answering'
if 'current_verb' not in st.session_state: st.session_state.current_verb = None
if 'last_result' not in st.session_state: st.session_state.last_result = None
if 'start_time' not in st.session_state: st.session_state.start_time = time.time() # 開始時間
if 'end_time' not in st.session_state: st.session_state.end_time = None

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

# === C. ゲーム終了画面（10問終了後） ===
if st.session_state.game_state == 'ending':
    st.balloons()
    st.header("🏆 試合終了 (Full Time)！")
    
    # 時間計算
    elapsed_time = st.session_state.end_time - st.session_state.start_time
    elapsed_str = f"{elapsed_time:.1f} 秒"
    
    # スコア計算
    # 総合点 = 100 - (ミスx5) - (時間/10)
    max_score = 100
    miss_penalty = st.session_state.misses * 5
    time_penalty = elapsed_time / 10
    total_score = max_score - miss_penalty - time_penalty
    
    # 表示
    c1, c2, c3 = st.columns(3)
    c1.metric("⏱️ 経過時間", elapsed_str)
    c2.metric("❌ ミス回数", f"{st.session_state.misses} 回")
    c3.metric("💯 総合スコア", f"{int(total_score)} 点")
    
    st.write(f"内訳: 100点 - ミス({miss_penalty}点) - タイム減点({int(time_penalty)}点)")
    
    # 激励メッセージ
    if total_score >= 80:
        st.success("素晴らしい！ プロ級のストライカーだ！")
        show_image_fuzzy("perfect")
    elif total_score >= 50:
        st.info("ナイスファイト！ その調子で練習しよう！")
        show_image_fuzzy("good")
    else:
        st.warning("もっと練習して、次はハットトリックを狙おう！")
    
    # リトライボタン
    if st.button("もう一度挑戦する (Restart)"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# === A/B. ゲームプレイ中 ===
else:
    col1, col2 = st.columns(2)
    col1.metric("得点", f"{st.session_state.score} 点")
    col2.metric("ラウンド", f"第 {st.session_state.round} / 10 節")

    if st.session_state.current_verb is None:
        st.session_state.current_verb = random.choice(verbs)
    verb = st.session_state.current_verb

    # === 結果画面 ===
    if st.session_state.game_state == 'result':
        result = st.session_state.last_result
        if result == 'correct':
            st.success("⚽ GOAL!!!")
            img_k = random.choice(["good", "perfect"])
            show_image_fuzzy(img_k)
            se_k = random.choice(["clap", "cheer"])
            play_sound_fuzzy(se_k)
            vc_k = random.choice(["good", "perfect"])
            play_sound_fuzzy(vc_k)
            st.balloons()
            st.markdown(f"**正解:** {verb['base']} → {verb['past']} → {verb['pp']}")
            play_tts(f"Good job! {verb['base']}, {verb['past']}, {verb['pp']}")
            
            if 'feedback_text' not in st.session_state:
                p_text = f"Praise student for {verb['base']} -> {verb['past']}. Soccer style. Japanese translation."
                feedback = get_coach_feedback(p_text)
                if not feedback: feedback = random.choice(backup_quotes)
                st.session_state.feedback_text = feedback
            st.info(f"🗣️ {st.session_state.feedback_text}")
        else:
            st.error("惜しい！")
            show_image_fuzzy("miss")
            play_sound_fuzzy("miss")
            st.markdown(f"**正解は:** {verb['past']} / {verb['pp']}")
            play_tts(f"The answer is {verb['past']}, and {verb['pp']}")

        # 次へボタン（10ラウンド目なら終了画面へ）
        if st.button("次の試合へ"):
            if st.session_state.round >= 10:
                st.session_state.end_time = time.time()
                st.session_state.game_state = 'ending'
            else:
                st.session_state.game_state = 'answering'
                st.session_state.round += 1
                st.session_state.current_verb = None
                if 'feedback_text' in st.session_state: del st.session_state.feedback_text
            st.rerun()

    # === 回答画面 ===
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
                    st.session_state.misses += 1 # ミスをカウント
                st.session_state.game_state = 'result'
                st.rerun()

st.write("")
st.caption("Produced by Kashiwa Yellow Army School")
