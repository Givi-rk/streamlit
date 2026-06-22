import streamlit as st
st.title("Student information form")
name=st.text_input("Enter your name:")
age=st.number_input("Enter age:",1,100)
course=st.selectbox("Course",["Python","Java","C++","Php"])
submit=st.button("Submit")
if submit:
    st.write("Student Added Successfully.")
    st.write("Name:",name)
    st.write("Age:",age)
    st.write("Selected Course:",course)