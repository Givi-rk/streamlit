import streamlit as st
import os
from db_connection import connection
UPLOAD_FOLDER="./uploads/assignments"
def student_page():
    st.subheader("📄Assignment Submission")
    with st.form("assignment", clear_on_submit=True):
        name=st.text_input("Name")
        roll=st.text_input("Roll Number")
        assignment=st.text_input("Assignment Title")
        subject=st.text_input("Subject")
        upload=st.file_uploader("Upload Assignment",type=["pdf","docx","zip"], max_upload_size=5, width=280)
        if st.form_submit_button("Submit"):
            if not all([name,roll,assignment,subject,upload]):
                st.warning("All fields are required.")
                return
            try:
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                filepath=os.path.join(UPLOAD_FOLDER,upload.name)
                with open(filepath,"wb") as f:
                    f.write(upload.getbuffer())
                conn,cursor=connection()
                cursor.execute("INSERT INTO assignments (name,roll_no,assignment_title,subject,uploaded_file) VALUES (%s,%s,%s,%s,%s)",(name,roll,assignment,subject,filepath))
                conn.commit()
                st.success("✅Assignment submitted successfully.")
            except Exception as e:
                st.error(e)
            finally:
                cursor.close()
                conn.close()