import streamlit as st

st.set_page_config(page_title="条件分岐入力アプリ", layout="centered")
st.title("データ入力アプリ")

# 1. 区分選択（ラジオボタン）
option_radio = st.radio("【1】 状態を選択", ["ふたば", "蕾", "花"], horizontal=True)
option_radio2 = st.radio("【2】 色を選択", ["不明", "白", "黃", "赤", "青"], horizontal=True)

# 送信時に使う変数の初期値をセット
my_value = 0
hours = 0
minutes = 0

# 2. 条件分岐による質問項目の切り替え
if option_radio == "ふたば" or option_radio == "蕾":
    my_value = st.number_input(
        "【3】 残り本数を入れてください（整数）", min_value=0, value=300, step=1
    )

else:
    # B, C, Dを選択した場合の表示項目
    st.write("【3】 残り時間")
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
st.write("【4】 花の種類選択")

if "flower_list" not in st.session_state:
    st.session_state.flower_list = ["ただの花", "ケイトウ", "トルコキキョウ"]

selected_flower = st.selectbox("アイテムを選択", st.session_state.flower_list)

with st.expander("＋ リストに新しく追加する"):
    new_flower = st.text_input("新しい項目を入力")
    if st.button("追加"):
        if new_flower and new_flower not in st.session_state.flower_list:
            st.session_state.fruit_list.append(new_flower)
            st.success(f"「{new_flower}」を追加しました！")
            st.rerun()
        elif new_flower in st.session_state.fruit_list:
            st.warning("その項目はすでに存在します。")

# 4. 送信処理
st.divider()
if st.button("送信・保存", type="primary", use_container_width=True):
    # ここでまとめてデータの送信・保存処理を行えます
    # （※ スプレッドシートなどに書き込む場合も、以下の変数を使用します）

    st.success("送信完了！送信されたデータは以下の通りです：")
    st.json(
        {
            "状態 (option_radio)": option_radio,
            "色 (option_radio2)": option_radio2,
            "残り本数 (my_value)": my_value,
            "時間 (hours)": hours,
            "分 (minutes)": minutes,
            "花の種類 (selected_flower)": selected_flower,
        }
    )