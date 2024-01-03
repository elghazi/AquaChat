from datetime import datetime
from enum import Enum
from pathlib import Path
import streamlit as st

class MODE(Enum):
    CHAT = 1
    UPLOAD = 2


base_dir = Path(__file__).parent.parent
reviews_dir = base_dir / "volume" / "reviews"
reviews_dir.resolve().mkdir(parents=True, exist_ok=True)
custom_icon_path = "assets/aquachat_assistant_icon01.2.jpg"
user_icon = "👤"


def upload_review():
    with st.form("upload_form", clear_on_submit=True):
        review = st.text_area("Review", key='review', height=100, placeholder="Please share you review here...")
        uploaded_files = st.file_uploader('Upload documents (optional)',
                                          type=['pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx', 'html', 'cvs'],
                                          key='file_upload_widget',
                                          accept_multiple_files=True)

        fullname = st.text_input('Full name', key='fullname', placeholder="Add your name")
        email = st.text_input('Email', key='email', placeholder="Add your email")
        affiliation = st.text_input('Affiliation', key='affiliation', placeholder="Add your company")

        # If a files were uploaded, display their contents
        if uploaded_files:
            st.write("Uploaded Files:")
            for file in uploaded_files:
                st.write(file.name)

        # Display a submit button
        submitted = st.form_submit_button('Submit review')
        if submitted:
            # Process and save the review
            save_review(review, fullname, email, affiliation, uploaded_files)
            # st.session_state.chat_mode = MODE.CHAT


def save_review(review, fullname, email, affiliation, files):
    # Check if both review content and files are empty
    if not review and not files:
        st.error('Please enter a review or upload a review document to submit', icon="🚨")
        return False

    # Create a unique directory for each review
    date_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")
    review_dir = reviews_dir / date_time
    review_dir.resolve().mkdir(parents=True, exist_ok=True)

    # Save review details to a text file
    review_file_path = review_dir / f"review-{date_time}.txt"
    with open(review_file_path, 'w') as f:
        f.write(f"Review Content:\n{review}\n\n")
        f.write(f"Full Name: {fullname}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Affiliation: {affiliation}\n")

    # Save uploaded files to the review directory
    if files:
        for file in files:
            file_path = review_dir / file.name
            with open(file_path, 'wb') as f:
                f.write(file.getbuffer())

    # Display success messages or other actions
    st.success('Thank you for your review!')
    st.toast('Review successfully submitted!')
    return True

def assistant_message(content):
    col1, col2 = st.columns([0.075, 1])  # Adjust the width ratio between icon and text as needed
    col1.image(custom_icon_path, width=25)
    col2.write(content)

st.title("💬 Aquadviser")
st.caption("An Aqua Chatbot powered by Aquadviser")


if "messages" not in st.session_state:
    st.session_state.chat_mode = MODE.CHAT
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        assistant_message(msg["content"])
    else:
        st.chat_message(user_icon).write(msg["content"])

if st.session_state.chat_mode.value == MODE.CHAT.value:
    prompt = st.chat_input()
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = "We're collecting reviews on water technologies. Feel free to share!"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.chat_mode = MODE.UPLOAD
        st.experimental_rerun()
elif st.session_state.chat_mode.value == MODE.UPLOAD.value:
    upload_review()
else:
    print(f"Mode {st.session_state.chat_mode} not supported!")

