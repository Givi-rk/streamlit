import mysql.connector
import streamlit as st
def connection():
    try:
        conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='assignment_management_system'
        )
        cursor=conn.cursor()
        return conn,cursor
    except mysql.connection.Error as e:
        st.error(f"Database Error:",{e})
        return None,None
    