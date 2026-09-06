import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

st.set_page_config(page_title="条件分岐入力アプリ", layout="centered")


# --- 1. Google スプレッドシート接続処理 ---
@st.cache_resource
def get_gspread_client():
    # スコープに drive を追加します
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials_dict = dict(st.secrets["gcp_service_account"])
    credentials_dict["private_key"] = credentials_dict[
        "private_key"
    ].replace("\\n", "\n")

    credentials = Credentials.from_service_account_info(
        credentials_dict, scopes=scopes
    )
    return gspread.authorize(credentials)


# スプレッドシートの取得関数
def get_worksheet():
    gc = get_gspread_client()
    # 接続したいGoogleスプレッドシートの名前を指定
    sh = gc.open("入力データ管理")
    return sh.sheet1


# --- 2. 画面UIと入力フォーム ---
st.title("データ入力アプリ")

# 区分選択
option_radio = st.radio("【1】 区分を選択", ["A", "B", "C", "D"], horizontal=True)

# 送信用変数の初期化
my_value = 0
hours = 0
minutes = 0

# 条件分岐による表示の切り替え
if option_radio == "A":
    st.info("※ 区分Aを選択したため、残り時間の入力は不要です。")
    my_value = st.number_input(
        "【2】 数値を入れてください（整数）", min_value=0, value=10, step=1
    )
else:
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

# フルーツ選択
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

# --- 3. 送信およびスプレッドシート書き込み処理 ---
st.divider()

if st.button("送信・保存", type="primary", use_container_width=True):
    # 送信するデータをリスト形式で準備（スプレッドシートの列の並び順に合わせます）
    row_data = [
        option_radio,  # 1列目: 区分
        my_value,  # 2列目: 数値 (A以外なら0)
        hours,  # 3列目: 時間 (Aなら0)
        minutes,  # 4列目: 分 (Aなら0)
        selected_fruit,  # 5列目: フルーツ
    ]

    try:
        # スプレッドシートを取得して末尾に行を追加
        worksheet = get_worksheet()
        worksheet.append_row(row_data)

        st.success("スプレッドシートへの保存が完了しました！")

        # 保存された内容を表示（確認用）
        st.json(
            {
                "区分 (option_radio)": option_radio,
                "数値 (my_value)": my_value,
                "時間 (hours)": hours,
                "分 (minutes)": minutes,
                "選択フルーツ (selected_fruit)": selected_fruit,
            }
        )

    except Exception as e:
        st.error(f"保存中にエラーが発生しました: {e}")