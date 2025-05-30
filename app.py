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

def get_workspace_name(org_id, api_key, token):
    url = f"https://api.trello.com/1/organizations/{org_id}"
    params = {"key": api_key, "token": token}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("displayName", "")
    return "（名前不明）"

def main():
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

        params = {"key": api_key, "token": token}
        response = requests.get("https://api.trello.com/1/members/me/boards", params=params)

        if response.status_code == 200:
            boards = response.json()
            # アーカイブ除外
            active_boards = [b for b in boards if not b.get("closed", False)]

            # ワークスペース名を取得して表示
            st.write("\n📋 有効なボード一覧（アーカイブ除外・全ワークスペース）：")
            for board in active_boards:
                org_id = board.get("idOrganization")
                ws_name = get_workspace_name(org_id, api_key, token) if org_id else "（ワークスペースなし）"
                st.markdown(f"- **{board['name']}**（ワークスペース：{ws_name}）")
        else:
            st.error("❌ Trello APIへの接続に失敗しました。キーやトークンを再確認してください。")

if __name__ == "__main__":
    main()
