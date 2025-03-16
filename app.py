from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Streamlit Community CloudのSecretsにOPENAI_API_KEYを設定しておく前提です
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# LLMの初期化（model_name等は必要に応じて変更してください）
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

def get_llm_response(input_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類に応じたシステムメッセージを元に、
    LangChainを通してLLMからの回答を取得する関数です。
    
    Parameters:
    - input_text: ユーザーが入力したテキスト（質問）
    - expert_type: ラジオボタンで選択した専門家の種類
    
    Returns:
    - LLMからの回答テキスト
    """
    # 専門家の種類に応じてシステムメッセージを設定
    if expert_type == "料理の専門家":
        system_message = "あなたは優秀な料理の専門家です。"
    elif expert_type == "健康の専門家":
        system_message = "あなたは優秀な健康の専門家です。"
    else:
        system_message = "あなたは優秀な専門家です。"
    
    # LangChain用のメッセージリストを作成
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]
    
    # LLMに問い合わせを実行
    response = llm(messages)
    return response.content

# StreamlitアプリのUI作成
st.title("LLMチャットアプリ")
st.write(
    """
    このアプリはLangChainとLLMを用いたチャットアプリです。  
    下記のフォームに質問を入力し、左側のラジオボタンで専門家の種類（**料理の専門家**または**健康の専門家**）を選択してください。  
    「実行」ボタンを押すと、選択された専門家の視点でLLMからの回答が表示されます。
    """
)

# ラジオボタンで専門家の種類を選択
expert_option = st.radio(
    "専門家の種類を選択してください。",
    ["料理の専門家", "健康の専門家"]
)

# 入力フォーム（質問を入力）
user_input = st.text_input("質問を入力してください。")

# 「実行」ボタン押下時の処理
if st.button("実行"):
    st.divider()
    if user_input.strip() == "":
        st.error("質問を入力してから「実行」ボタンを押してください。")
    else:
        with st.spinner("回答を生成中です..."):
            answer = get_llm_response(user_input, expert_option)
            st.write("#### LLMの回答")
            st.write(answer)
