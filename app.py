import streamlit as st
import requests
import json

# إعداد عنوان الصفحة
st.set_page_config(page_title="Medical ChatBot", layout="wide")
st.title("💬 Medical AI Chatbot")

# تحميل مفتاح API ورابط API من secrets.toml
dify_api_key = st.secrets["dify"]["api_key"]
dify_api_url = st.secrets["dify"]["api_url"]

# تهيئة حالة الجلسة لتخزين سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "مرحبًا! كيف يمكنني مساعدتك؟"}]

# عرض سجل المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة رسالة المستخدم إلى سجل المحادثة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # إرسال الطلب إلى Dify API
    headers = {
        "Authorization": f"Bearer {dify_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": prompt,
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "user_id"  # يمكنك تخصيص معرف المستخدم إذا لزم الأمر
    }

    try:
        # إرسال الطلب إلى Dify
        response = requests.post(dify_api_url, headers=headers, json=payload, stream=True)
        response.raise_for_status()

        # قراءة الرد المتدفق (Streaming) من Dify
        bot_response = ""
        with st.chat_message("assistant"):
            placeholder = st.empty()
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        # معالجة البيانات المتدفقة
                        chunk_data = json.loads(chunk.decode("utf-8").replace("data: ", ""))
                        if chunk_data.get("event") == "message":
                            bot_response += chunk_data["answer"]
                            placeholder.write(bot_response)
                    except json.JSONDecodeError:
                        continue

        # إضافة رد البوت إلى سجل المحادثة
        st.session_state.messages.append({"role": "assistant", "content": bot_response])

    except requests.exceptions.RequestException as e:
        st.error(f"حدث خطأ أثناء الاتصال بـ Dify API: {e}")