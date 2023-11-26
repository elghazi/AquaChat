import streamlit as st
import pandas as pd
import os
from io import StringIO
from pathlib import Path
from datetime import datetime

# page layout config
st.set_page_config(layout='wide')
st.title("Submit a review")
st.caption("We're collecting reviews on water technologies. Feel free to share here!.")

base_dir = Path(__file__).parent.parent 
reviews_dir = os.path.join(base_dir, 'volume\\reviews')
    
def save_files():
    files = st.session_state.file_upload_widget
 
    #if(len(st.session_state.fullname) == 0):
    #    st.error('Field Fullname is required', icon="🚨")
    #    return False
    #if(len(st.session_state.review) == 0):
    #    st.error('Please enter a Review to submit', icon="🚨")
    #    return False    
    
    if(len(st.session_state.review) == 0 and len(files) == 0):
        st.error('Please enter a review or upload a review document to submit', icon="🚨")
        return False    

    date_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")

    # creates a new review directory
    review_dir = reviews_dir + '\\' + date_time
    os.mkdir(review_dir) 

    with open(os.path.join(review_dir, 'review-' + date_time + '.txt'), 'w') as f:
        if(len(st.session_state.fullname) > 0):
            f.write('Fullname:\n')
            f.write(st.session_state.fullname)
        if(len(st.session_state.contact) > 0):
            f.write('\n\nContact:\n')
            f.write(st.session_state.contact)
        if(len(st.session_state.review) > 0):
            f.write('\n\nReview:\n')
            f.write(st.session_state.review)

    if len(files) > 0:
        for file in files:
            with open(os.path.join(review_dir, file.name), 'wb') as f:
                f.write(file.getbuffer())
                
    st.success('Review successfully sumbitted!', icon="✅")
    st.toast('Thank you for submitting the review!')
    return True
  
def main():
    with st.form("upload_form", clear_on_submit = True):
        #fullname = st.text_input('Fullname*', '', key = 'fullname')
        review = st.text_area("Review", key = 'review', height=300, placeholder="Please share you review here...")
        uploaded_files = st.file_uploader('Upload review related documents (optional)',
                                          type=['pdf', 'txt', 'doc', 'docx', 'tex'],
                                          key='file_upload_widget',
                                          accept_multiple_files=True)
   
        contact = st.text_area('Contact', key = 'contact', placeholder="Add some optional contact information")
        # If a files was uploaded, display its contents
        submitted = st.form_submit_button('Submit review', on_click=save_files)

main()