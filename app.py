import streamlit as st
import requests

https://udify.app/chat/oVcUygy5KwCUi0Qn
API_URL = https://api.dify.ai/v1
API_KEY = app-GLbTJRnrEX6c7q5v5AZYH9ac

st.title("MedicalChatBot")

user_input = st.text_input("اكتب سؤالك:")

if st.button("إرسال"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": user_input
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json().get("answer", "لا يوجد رد.")
        st.success(reply)
    else:
        st.error("فشل الاتصال بـ Dify.")