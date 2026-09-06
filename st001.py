import streamlit as st

# 1. 画面表示の最適化（スマホ向けビューポート設定）
st.set_page_config(page_title="データ入力", layout="centered")

st.title("データ入力")

# 2. ラジオボタン（A, B, C, D）
# 横並びにしたい場合は horizontal=True を設定
option_radio = st.radio("【1】 色を選択", ["白", "黃", "赤", "青"], horizontal=True)

# 3. 残り時間（時間・分の数値入力）
st.write("【2】 残り時間")
col1, col2 = st.columns(2)
with col1:
    hours = st.number_input("時間", min_value=0, max_value=99, value=3, step=1)
with col2:
    minutes = st.number_input("分", min_value=0, max_value=59, value=20, step=1)

# 4. 動的な選択肢（コンボボックス＋新規追加機能）
st.write("【3】 フルーツ選択")

# セッション状態（st.session_state）で選択肢を保持
if "fruit_list" not in st.session_state:
    st.session_state.fruit_list = ["apple", "banana", "cherry"]

# 選択ボックス
selected_fruit = st.selectbox("アイテムを選択", st.session_state.fruit_list)

# 選択肢の動的追加（アコーディオン内に配置）
with st.expander("＋ リストに新しく追加する"):
    new_fruit = st.text_input("新しい項目を入力")
    if st.button("追加"):
        if new_fruit and new_fruit not in st.session_state.fruit_list:
            st.session_state.fruit_list.append(new_fruit)
            st.success(f"「{new_fruit}」を追加しました！")
            st.rerun()  # 画面を再描画して選択肢を更新
        elif new_fruit in st.session_state.fruit_list:
            st.warning("その項目はすでに存在します。")

# 送信ボタン
st.divider()
if st.button("送信・保存", type="primary", use_container_width=True):
    st.success(
        f"送信完了: {option_radio} / {hours}時間{minutes}分 / {selected_fruit}"
    )
