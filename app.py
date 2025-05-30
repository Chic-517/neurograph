import streamlit as st
import requests
import json
import os

CREDENTIAL_FILE = "credentials.json"

def load_credentials():
    if os.path.exists(CREDENTIAL_FILE):
        with open(CREDENTIAL_FILE, "r") as f:
            return json.load(f)
    return {"api_key": "", "token": ""}

def save_credentials(api_key, token):
    with open(CREDENTIAL_FILE, "w") as f:
        json.dump({"api_key": api_key, "token": token}, f)

cred = load_credentials()

st.title("🔐 NeuroGraph Preview - Trello連携")

st.markdown("""
💡 TrelloのAPIキーとトークンは以下から取得できます：

- 🔑 [Trello APIキーを取得](https://trello.com/app-key)
- 🔐 「Tokenを生成」のリンクをクリックしてトークン取得
""")

api_key = st.text_input("APIキー", value=cred["api_key"], placeholder="例: 123abc456...", max_chars=64)
token = st.text_input("トークン", value=cred["token"], placeholder="例: abc123xyz...", type="password", max_chars=128)

if api_key and token:
    save_credentials(api_key, token)
    st.success("✅ キーとトークンが入力・保存されました！")

    params = {'key': api_key, 'token': token}
    response = requests.get("https://api.trello.com/1/members/me/boards", params=params)

    if response.status_code == 200:
        boards = response.json()

        # ✅ 表示を許可するワークスペースのID（※仮IDなので本物に置き換えてね）
        allowed_workspace_ids = [
            "org_id_neurograph_123",
            "org_id_osusumeya_456"
        ]

        st.write("📋 あなたのTrelloボード一覧（ワークスペース制限 & アーカイブ除外）：")
        for board in boards:
            if (
                board.get("idOrganization") in allowed_workspace_ids and
                not board.get("closed", False)
            ):
                st.markdown(f"- {board['name']}")
    else:
        st.error("❌ Trello APIへの接続に失敗しました。キーやトークンを再確認してください。")
