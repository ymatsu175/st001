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

# スプレッドシート全体を取得
@st.cache_resource
def get_spreadsheet():
    gc = get_gspread_client()
    return gc.open("入力データ管理")  # スプレッドシート名


try:
    sh = get_spreadsheet()

    worksheet_data = sh.worksheet("ログ")
    worksheet_flower = sh.worksheet("花候補")
    worksheet_place = sh.worksheet("場所候補")

    # シート2のA列（1列目）から選択肢を取得（空文字を除外）
    # ※1行目がヘッダー（「フルーツ名」等）の場合は [1:] で除外します
    flower_column_values = worksheet_flower.col_values(1)
    # 1行目が見出しなら fruit_column_values[1:] に変更してください
    flower_list = [v for v in flower_column_values if v.strip() != ""]

    if not flower_list:
        flower_list = ["（選択肢がありません）"]

    place_column_values = worksheet_place.col_values(1)
    place_list = [v for v in place_column_values if v.strip() != ""]
    if not place_list:
        place_list = ["（選択肢がありません）"]

except Exception as e:
    st.error(f"スプレッドシートの読み込みに失敗しました: {e}")
    st.stop()

# --- 2. 画面UIと入力フォーム ---
st.title("データ入力アプリ")

# 場所の選択
st.write("【1】 場所の選択")
selected_place = st.selectbox("アイテムを選択", place_list)

# 状態と色の選択
option_radio = st.radio("【2】 状態を選択", ["ふたば", "蕾", "花"], horizontal=True)
option_radio2 = st.radio("【3】 色を選択", ["不明", "白", "黃", "赤", "青"], horizontal=True)

# 送信用変数の初期化
my_value = 0
hours = 0
minutes = 0

# 条件分岐による表示の切り替え
if option_radio == "ふたば" or option_radio == "蕾":
    my_value = st.number_input(
        "【4】 残り本数を入れてください（整数）", min_value=0, value=300, step=1
    )
else:
    # B, C, Dを選択した場合の表示項目
    st.write("【4】 残り時間")
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
st.write("【5】 花の種類選択")
#selected_flower = st.selectbox("アイテムを選択", st.session_state.flower_list)
selected_flower = st.selectbox("アイテムを選択", flower_list)

# --- 3. 送信およびスプレッドシート書き込み処理 ---
st.divider()

import datetime

if "dt_now_old" not in st.session_state:
    st.session_state.dt_now_old= datetime.datetime.now()

if st.button("送信・保存", type="primary", use_container_width=True):
    # 送信するデータをリスト形式で準備（スプレッドシートの列の並び順に合わせます）
    dt_now= datetime.datetime.now()
    #print(dt_now_old.timestamp())
    #print(dt_now.timestamp()-10)
    if st.session_state.dt_now_old.timestamp() < dt_now.timestamp()-10:
    #if True:
        row_data = [
            dt_now.strftime('%Y-%m-%d %H:%M:%S'), # 現在時刻
            selected_place,  # 1列目: 場所
            option_radio,  # 2列目: 状態
            option_radio2,  # 3列目: 色
            my_value,  # 4列目: 残り本数 (花なら0)
            hours,  # 5列目: 時間 (ふたば、蕾なら0)
            minutes,  # 6列目: 分 (ふたば、蕾ならなら0)
            selected_flower,  # 7列目: 花の種類
        ]
        st.session_state.dt_now_old= dt_now

        try:
            # スプレッドシートを取得して末尾に行を追加
            #worksheet = get_worksheet()
            worksheet_data.append_row(row_data)

            st.success("スプレッドシートへの保存が完了しました！")

            # 保存された内容を表示（確認用）
            dmy= r'''
            st.json(
                {
                    "日時 (now)": now,
                    "状態 (option_radio)": option_radio,
                    "色 (option_radio2)": option_radio2,
                    "残り本数 (my_value)": my_value,
                    "時間 (hours)": hours,
                    "分 (minutes)": minutes,
                    "花の種類 (selected_flower)": selected_flower,
                }
            )
            '''

        except Exception as e:
            st.error(f"保存中にエラーが発生しました: {e}")
    #else:
    #    print('連打？')