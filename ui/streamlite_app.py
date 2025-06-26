import streamlit as st
import requests

API_URL = "http://localhost:8000"


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def add_to_history(user_question, ai_answer):
    st.session_state.chat_history.append({'question': user_question, 'answer': ai_answer})

st.title("📄 AI PDF Assistant")


# Upload section
st.subheader("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF or scanned image", type=["pdf", "png", "jpg"])
api_key = st.text_input("Enter your API Key", type="password")

if uploaded_file and api_key:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    headers = {"X-API-Key": api_key}
    with st.spinner("Uploading..."):
        response = requests.post(f"{API_URL}/upload", files=files, headers=headers)
    if response.status_code == 200:
        st.success("✅ Document uploaded and processed!")
    else:
        st.error(f"❌ Upload failed: {response.text}")

# Ask section
st.subheader("Ask a Question")
query = st.text_input("What do you want to know about the document?")

if st.button("Ask") and query and api_key:
    headers = {"X-API-Key": api_key}
    response = requests.post(f"{API_URL}/ask", json={"question": query}, headers=headers)
    if response.status_code == 200:
        st.markdown(f"**Answer:** {response.json()['answer']}")
    else:
        st.error(f"❌ Error: {response.text}")
