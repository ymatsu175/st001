import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

st.set_page_config(page_title="PM入力アプリ", layout="centered")


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

# 状態と色の選択
option_radio = st.radio("【1】 状態を選択", ["ふたば", "蕾", "花"], horizontal=True)
option_radio2 = st.radio("【2】 色を選択", ["不明", "白", "黃", "赤", "青"], horizontal=True)

# 送信用変数の初期化
my_value = 0
hours = 0
minutes = 0

# 条件分岐による表示の切り替え
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

# 花の種類選択
st.write("【4】 花の種類選択")
if "flower_list" not in st.session_state:
    st.session_state.flower_list = ["ただの花", "ケイトウ", "トルコキキョウ"]

selected_flower = st.selectbox("アイテムを選択", st.session_state.flower_list)

with st.expander("＋ リストに新しく追加する"):
    new_flower = st.text_input("新しい項目を入力")
    if st.button("追加"):
        if new_flower and new_flower not in st.session_state.flower_list:
            st.session_state.flower_list.append(new_flower)
            st.success(f"「{new_flower}」を追加しました！")
            st.rerun()
        elif new_flower in st.session_state.flower_list:
            st.warning("その項目はすでに存在します。")

# --- 3. 送信およびスプレッドシート書き込み処理 ---
st.divider()

if st.button("送信・保存", type="primary", use_container_width=True):
    # 送信するデータをリスト形式で準備（スプレッドシートの列の並び順に合わせます）
    row_data = [
        option_radio,  # 1列目: 状態
        option_radio2,  # 2列目: 色
        my_value,  # 3列目: 残り本数 (花なら0)
        hours,  # 4列目: 時間 (ふたば、蕾なら0)
        minutes,  # 5列目: 分 (ふたば、蕾ならなら0)
        selected_flower,  # 6列目: 花の種類
    ]

    try:
        # スプレッドシートを取得して末尾に行を追加
        worksheet = get_worksheet()
        worksheet.append_row(row_data)

        st.success("スプレッドシートへの保存が完了しました！")

        # 保存された内容を表示（確認用）
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

    except Exception as e:
        st.error(f"保存中にエラーが発生しました: {e}")