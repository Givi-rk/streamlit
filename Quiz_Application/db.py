import mysql.connector
import streamlit as st
def connection():
    try:
        conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='students_database'
        )
        cursor=conn.cursor()
        return conn,cursor
    except mysql.connector.Error as e:
        st.error("Database Error:",e)
        return None,None