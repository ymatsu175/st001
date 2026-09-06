import streamlit as st

st.set_page_config(page_title="条件分岐入力アプリ", layout="centered")
st.title("データ入力アプリ")

# 1. 区分選択（ラジオボタン）
option_radio = st.radio("【1】 区分を選択", ["A", "B", "C", "D"], horizontal=True)

# 送信時に使う変数の初期値をセット
my_value = 0
hours = 0
minutes = 0

# 2. 条件分岐による質問項目の切り替え
if option_radio == "A":
    # Aを選択した場合の表示項目
    st.info("※ 区分Aを選択したため、残り時間の入力は不要です。")
    my_value = st.number_input(
        "【2】 数値を入れてください（整数）", min_value=0, value=10, step=1
    )

else:
    # B, C, Dを選択した場合の表示項目
    st.write("【2】 残り時間")
    col1, col2 = st.columns(2)
    with col1:
        hours = st.number_input(
            "時間", min_value=0, max_value=99, value=3, step=1
        )
    with col2:
        minutes = st.number_input(
            "分", min_value=0, max_value=59, value=20, step=1
        )

# 3. フルーツ選択（コンボボックス＋新規追加）
st.write("【3】 フルーツ選択")

if "fruit_list" not in st.session_state:
    st.session_state.fruit_list = ["apple", "banana", "cherry"]

selected_fruit = st.selectbox("アイテムを選択", st.session_state.fruit_list)

with st.expander("＋ リストに新しく追加する"):
    new_fruit = st.text_input("新しい項目を入力")
    if st.button("追加"):
        if new_fruit and new_fruit not in st.session_state.fruit_list:
            st.session_state.fruit_list.append(new_fruit)
            st.success(f"「{new_fruit}」を追加しました！")
            st.rerun()
        elif new_fruit in st.session_state.fruit_list:
            st.warning("その項目はすでに存在します。")

# 4. 送信処理
st.divider()
if st.button("送信・保存", type="primary", use_container_width=True):
    # ここでまとめてデータの送信・保存処理を行えます
    # （※ スプレッドシートなどに書き込む場合も、以下の変数を使用します）

    st.success("送信完了！送信されたデータは以下の通りです：")
    st.json(
        {
            "区分 (option_radio)": option_radio,
            "数値 (my_value)": my_value,
            "時間 (hours)": hours,
            "分 (minutes)": minutes,
            "選択フルーツ (selected_fruit)": selected_fruit,
        }
    )