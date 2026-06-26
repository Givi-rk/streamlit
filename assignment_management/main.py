import streamlit as st
from student import student_page
from teacher import teacher_page
if "page" not in st.session_state:
     st.session_state.page="home"
def page():
    st.set_page_config(
        page_title="Assignments",
        page_icon="📑",
        layout="wide"
    )
    if st.session_state.page=="home":
            st.markdown("""<style>
                         .title{
                        text-align:center;
                        font-size:50px;
                        font-weight:bold;
                        margin-bottom:20px;
                        }
                        .subheader{
                        text-align:center;
                        font-size:30px;
                        margin-bottom:20px;
                        }""",unsafe_allow_html=True)
            st.markdown("<div class=title>HELLO,THERE</div>",unsafe_allow_html=True)
            st.markdown("<div class=subheader>Welcome to Assignment management system</div>",unsafe_allow_html=True)
            st.markdown("<h5 style='text-align:center;margin-bottom:30px'>Choose your role below to continue</h3>",unsafe_allow_html=True)
            c1,c2,c3,c4=st.columns(4)
            if c2.button("Log in as 👩🏻‍🎓 student",use_container_width=True):
                st.session_state.page="student"
                st.rerun()
            if c3.button("Log in as 👩🏻‍🏫teacher",use_container_width=True):
                st.session_state.page="teacher"
                st.rerun()
    if st.session_state.page=="student":
        if st.button("⬅️🏠 Home"):
            st.session_state.page="home"
            st.rerun()
        student_page()
    if st.session_state.page=="teacher":
        if st.button("⬅️🏠 Home"):
            st.session_state.page="home"
            st.rerun()
        teacher_page()
page()
