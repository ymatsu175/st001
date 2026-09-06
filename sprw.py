import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

st.title("スプレッドシート連携アプリ")

# Secretsから認証情報を読み込む関数
@st.cache_resource
def get_gspread_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    # SecretsからJSONキーの辞書を取得
    credentials_dict = dict(st.secrets["gcp_service_account"])
    # private_key の改行コード調整（Secrets入力時の改行崩れ防止）
    credentials_dict["private_key"] = credentials_dict[
        "private_key"
    ].replace("\\n", "\n")

    credentials = Credentials.from_service_account_info(
        credentials_dict, scopes=scopes
    )
    return gspread.authorize(credentials)


try:
    gc = get_gspread_client()

    # スプレッドシート名（またはキー）を指定して開く
    # ※共有設定をしたスプレッドシート名を指定してください
    sh = gc.open("入力データ管理")
    worksheet = sh.sheet1

    # 既存データの取得
    data = worksheet.get_all_records()
    st.subheader("現在のデータ")
    st.dataframe(data)

    # データ追加の例
    with st.form("input_form"):
        item = st.text_input("項目名")
        value = st.number_input("数値", min_value=0)
        submitted = st.form_submit_button("スプレッドシートに保存")

        if submitted:
            worksheet.append_row([item, value])
            st.success("スプレッドシートに書き込みました！")
            st.rerun()

except Exception as e:
    st.error(f"エラーが発生しました: {e}")