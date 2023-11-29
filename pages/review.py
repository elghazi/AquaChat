import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# page layout config
st.set_page_config(layout='wide')
st.title("Submit a review")
st.caption("We're collecting reviews on water technologies. Feel free to share here!.")

base_dir = Path(__file__).parent.parent
reviews_dir = base_dir / "volume" / "reviews"
reviews_dir.resolve().mkdir(parents=True, exist_ok=True)


def save_files():
    files = st.session_state.file_upload_widget

    if (len(st.session_state.review) == 0 and len(files) == 0):
        st.error('Please enter a review or upload a review document to submit', icon="🚨")
        return False

    date_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")

    # creates a new review directory
    review_dir = reviews_dir / date_time
    review_dir.resolve().mkdir(parents=True, exist_ok=True)
    review_file_path = review_dir / f"review-{date_time}.txt"
    with open(review_file_path, 'w') as f:
        if (len(st.session_state.fullname) > 0):
            f.write('\n\nFullname:\n')
            f.write(st.session_state.fullname)
        if (len(st.session_state.email) > 0):
            f.write('\n\nEmail:\n')
            f.write(st.session_state.email)
        if (len(st.session_state.affiliation) > 0):
            f.write('\n\nAffiliation:\n')
            f.write(st.session_state.affiliation)
        if (len(st.session_state.review) > 0):
            f.write('\n\nReview:\n')
            f.write(st.session_state.review)

    # if len(files) > 0:
    for file in files:
        with open(review_dir / file.name, 'wb') as f:
            f.write(file.getbuffer())

    st.success('Review successfully sumbitted!', icon="✅")
    st.toast('Thank you for submitting the review!')
    return True


def main():
    with st.form("upload_form", clear_on_submit=True):
        review = st.text_area("Review", key='review', height=300, placeholder="Please share you review here...")
        uploaded_files = st.file_uploader('Upload documents (optional)',
                                          type=['pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx', 'html', 'cvs'],
                                          key='file_upload_widget',
                                          accept_multiple_files=True)

        fullname = st.text_input('Full name',  key='fullname', placeholder="Add your name")
        email = st.text_input('Email', key='email', placeholder="Add your email")
        affiliation = st.text_input('Affiliation', key='affiliation', placeholder="Add your company")
        # If a files was uploaded, display its contents
        submitted = st.form_submit_button('Submit review', on_click=save_files)


main()