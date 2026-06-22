import streamlit as st
st.title("To Do List")
task=st.text_input("Enter your task:")
if st.button("Add task"):
    st.write("Task added:",task)