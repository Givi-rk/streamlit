import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from reportlab.platypus import SimpleDocTemplate,Table
if "page" not in st.session_state:
    st.session_state.page="dashboard"
try:
    conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='students_database'
)
    cursor=conn.cursor()
except mysql.connector.Error as e:
    st.error("Error:",e)
def page():
    st.set_page_config(page_title="Student Portal",layout="wide")
    with st.container():
        c1,c2,c3,c4=st.columns([7,1,1,1])
        with c1:
            st.text_input("",placeholder="🔍 Global Search")
        with c2:
            st.write("")
            st.write("")
            st.button("🔔")
        with c3:
            st.write("")
            st.write("")
            st.button("❓")
        with c4:
            st.write("")
            st.write("")
            st.button("| 👩‍💼")
        st.divider()

    #-----------sidebar------------
    with st.sidebar:
        st.title("AES")
        st.caption("ADMIN PORTAL")
        if st.button("📊DashBoard",use_container_width=True):
            st.session_state.page="dashboard"
        if st.button("👤+ Add Student",use_container_width=True):
            st.session_state.page="add student"
        if st.button("👥 View Students",use_container_width=True):
            st.session_state.page="view"
        if st.button("🔍 Search Student",use_container_width=True):
            st.session_state.page="search"
        if st.button("⚙️ Settings",use_container_width=True):
            st.session_state.page="setting"
        st.write("")
        st.write("")
        st.write("")
        st.subheader("Admin User")
        st.write("admin12@aes.edu")
    if st.session_state.page=="dashboard":
        dashboard()
    if st.session_state.page=="add student":
        add_student()
    if st.session_state.page=="view":
        view()
    if st.session_state.page=="details":
        details()
    if st.session_state.page=="setting":
        st.title("Setting")
    if st.session_state.page=="search":
        search_delete()
    if st.session_state.page=="edit":
        edit()
def dashboard():
    st.write("Portal > Dashboard")
    st.subheader("INSTITUTIONAL OVERVIEW")
    st.caption("Real-time performance metrics and administrative control for the Academic Excellence System.")
    c1,c2=st.columns([8,3])
    with c1:
        with st.container(border=True):
            left,mid,right=st.columns([3,4,2])
            with left:
                st.markdown("**Recent Enrollments**")
            with right:
                st.write("View All")
            cursor.execute("SELECT * FROM students")
            data=cursor.fetchall()
            df=pd.DataFrame(data,columns=["ID","STUDENT ID","NAME","EMAIL","PHONE","COURSE","STATUS","TIMESTAMP"])
            st.table(df)
    with c2:
        with st.container(border=True):
            st.write("🟢")
            st.write("ACTIVE STUDENTS")
            cursor.execute("SELECT COUNT(*) FROM students WHERE status='Active'")
            status=cursor.fetchone()[0]
            st.markdown(f"**{status}**")
        with st.container(border=True):
            st.write("❗")
            st.write("INACTIVE STUDENTS")
            cursor.execute("SELECT COUNT(*) FROM students WHERE status='Inactive'")
            status=cursor.fetchone()[0]
            st.markdown(f"**{status}**")
        with st.container(border=True):
            col1,col2=st.columns([4,1])
            with col1:
                st.write("📖")
                st.caption("TOTAL COURSES")
                cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
                count=cursor.fetchone()[0]
                st.markdown(f"**{count}**")
            with col2:
                st.write("...")
    with st.container(border=True):
        cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course")
        data=cursor.fetchall()
        courses=[row[0] for row in data]
        count=[row[1] for row in data]
        fig=px.bar(x=courses,
                y=count)
        st.plotly_chart(fig,use_container_width=True)
def add_student():
    st.set_page_config(
        page_title="Registration"
    )
    with st.container(border=True):
        c1,c2=st.columns([1,5])
        with c1:
            st.image("https://cdn-icons-png.flaticon.com/128/1144/1144760.png")
        with c2:
            st.subheader("Student Registration")
            st.caption("Fill in the official details to enroll a new student into the Aes system.")
        left,right=st.columns(2)
        with left:
            student_id=st.text_input("STUDENT ID")
            email=st.text_input("EMAIL ADDRESS")
            course=st.selectbox("COURSE PROGRAM",["Select a course","Computer Science Engineering","Civil Engineering","Mechanical Engineering","Electronics and Communication Engineering","Electrical Engineering"])
        with right:
            name=st.text_input("FULL NAME")
            phone=st.text_input("PHONE NUMBER",)
            st.write("ENROLLMENT STATUS")
            status_toggle=st.toggle("Active",value=True)
            status="Active" if status_toggle else "Inactive"
        st.text_input("INTERNAL ADMINISTRATIVE NOTES (OPTIONAL)",placeholder="Additional details about the student admission..")
        col1,col2=st.columns([3,2])
        with col1:
            if st.button("✅ Register Student"):
                cursor.execute("INSERT INTO students (student_id,name,email,phone,course,status) VALUES(%s,%s,%s,%s,%s,%s)",(student_id,name,email,phone,course,status,))
                if course=="Select a course":
                    st.error("Please select a course.")
                else:
                    conn.commit()
                    st.success("Registration Successful")
                    st.rerun()
        with col2:
            if st.button("♻️ Clear Form"):
                st.session_state.page="add student"
                st.rerun()
def view():
    st.subheader("Student Records")
    c1,c2,c3=st.columns([4,2,2])
    with c1:
        st.caption("Manage and view all student profiles across all departments.")
    with c2:
        if st.button("📥 Export to PDF"):
            export_pdf()
            with open("students_report.pdf","rb") as pdf_file:
                st.download_button(
                    label="⬇️ Download Pdf",
                    data=pdf_file,
                    file_name="students_report.pdf",
                    mime="application/pdf"
                )
                st.success("Pdf exported successfully.")
    with c3:
        if st.button("+ New student"):
            st.session_state.page="add student"
            st.rerun()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        course=st.selectbox("FILTER BY COURSE",["All courses","Computer Science Engineering","Civil Engineering","Mechanical Engineering","Electronics and Communication Engineering","Electrical Engineering"])
    with col2:
        status=st.selectbox("Account status",["Any status","Active","Inactive"])
    with col3:
        order=st.selectbox("Sort Order",["ID descending","ID ascending"])
    with col4:
        with st.container(border=True):
            st.markdown("**TOTAL ENROLLED**")
            cursor.execute("SELECT COUNT(*) FROM students")
            st.markdown(f"**{cursor.fetchone()[0]}**")
        cursor.execute("SELECT id,student_id,name,email,phone,course,status FROM students ORDER BY id DESC")
        students=cursor.fetchall()
    with st.container(border=True):
        in1,in2,in3,in4,in5,in6,in7,in8=st.columns([1,3,3,3,3,3,3,2])
        with in1:
            st.markdown("**ID**")
        with in2:
            st.markdown("**STUDENT_ID**")
        with in3:
            st.markdown("**NAME**")
        with in4:
            st.markdown("**EMAIL**")
        with in5:
            st.markdown("**PHONE**")
        with in6:
            st.markdown("**COURSE**")
        with in7:
            st.markdown("**STATUS**")
        with in8:
            st.markdown("**VIEW**")
        st.divider()
        for student in students:
            c1,c2,c3,c4,c5,c6,c7,c8=st.columns([1,3,3,3,3,3,3,2])
            c1.write(student[0])
            c2.write(student[1])
            c3.write(student[2])
            c4.write(student[3])
            c5.write(student[4])
            c6.write(student[5])
            c7.write(student[6])
            with c8:
                if st.button("View",key=f"view_{student[0]}"):
                    st.session_state.selected_students=student[0]
                    st.session_state.page="details"
                    st.rerun()
    l1,r1=st.columns(2)
    with l1:
        with st.container(border=True):
            st.write("📈 Growth Index")
            st.write("Student enrollment has increased by 8.2% compared to last semester,with the highest concentration in Computer Science modules.")
    with r1:
        with st.container(border=True):
            st.write("System Health")
            st.write("All database synchronization tasls are up to date. Last backup performed:24 min ago")
def details():
    if st.button("⬅️ Back"):
        st.session_state.page="view"
        st.rerun()
    with st.container(border=True):
        student_id=st.session_state.selected_students
        cursor.execute("SELECT * FROM students WHERE id=%s",(student_id,))
        profile=cursor.fetchone()
        st.subheader("👩🏻‍💻STUDENT DETAILS")
        st.markdown(f"**ID:** {student_id}")
        st.markdown(f"**STUDENT ID:** {profile[1]}")
        st.markdown(f"**NAME:** {profile[2]}") 
        st.markdown(f"**EMAIL:** {profile[3]}")
        st.markdown(f"**PHONE:** {profile[4]}")
        st.markdown(f"**COURSE:** {profile[5]}")
        st.markdown(f"**STATUS:** {profile[6]}")
def search_delete():
    search=st.text_input("🔍 Search by id or name...")
    if search:
        search_term=f"%{search}%"
        cursor.execute("SELECT * FROM students WHERE student_id LIKE %s OR name LIKE %s",(search_term,search_term))
        result=cursor.fetchall()
        if not result:
            st.info("Student not found!")       
        else:
            for student in result:
                left,mid,right=st.columns([6,3,3])
                with mid:
                    if st.button("✏️ Edit Info",key=f"edit_{student[0]}"):
                        st.session_state.edit_id=student[0]
                        st.session_state.page="edit"
                        st.rerun()
                st.subheader("👩🏻‍💻STUDENT DETAILS")
                st.markdown(f"**ID:** {student[0]}")
                st.markdown(f"**STUDENT ID:** {student[1]}")
                st.markdown(f"**NAME:** {student[2]}") 
                st.markdown(f"**EMAIL:** {student[3]}")
                st.markdown(f"**PHONE:** {student[4]}")
                st.markdown(f"**COURSE:** {student[5]}")
                st.markdown(f"**STATUS:** {student[6]}")
                with right:
                    if st.button("🗑️ Delete",key=f"delete_{student[0]}"):
                        cursor.execute("DELETE FROM students WHERE id=%s",(student[0],))
                        conn.commit()
                        st.session_state.pop("search_student",None)
                        st.success("Student deleted successfully.")

def edit():
    if "edit_id" not in st.session_state:
        st.error("No student selected.")
        return
    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (st.session_state.edit_id,)
    )
    student = cursor.fetchone()
    if not student:
        st.error("Student not found.")
        return
    with st.container(border=True):
        c1, c2 = st.columns([1, 5])
        with c1:
            st.image("https://cdn-icons-png.flaticon.com/128/1144/1144760.png")
        with c2:
            st.subheader("✏️ Edit Info")
        left, right = st.columns(2)
        with left:
            student_id = st.text_input(
                "STUDENT ID",
                value=student[1]
            )
            email = st.text_input(
                "EMAIL ADDRESS",
                value=student[3]
            )
            courses = [
                "Computer Science Engineering",
                "Civil Engineering",
                "Mechanical Engineering",
                "Electronics and Communication Engineering",
                "Electrical Engineering"
            ]
            course = st.selectbox(
                "COURSE PROGRAM",
                courses,
                index=courses.index(student[5])
                if student[5] in courses else 0
            )
        with right:
            name = st.text_input(
                "FULL NAME",
                value=student[2]
            )
            phone = st.text_input(
                "PHONE NUMBER",
                value=student[4]
            )
            st.write("ENROLLMENT STATUS")
            status_toggle = st.toggle(
                "Active",
                value=(student[6] == "Active")
            )
        status = "Active" if status_toggle else "Inactive"
        col1, col2 = st.columns([3, 2])
        with col1:
            if st.button("✅ Submit"):
                cursor.execute(
                    """
                    UPDATE students
                    SET student_id=%s,
                        name=%s,
                        email=%s,
                        phone=%s,
                        course=%s,
                        status=%s
                    WHERE id=%s
                    """,
                    (
                        student_id,
                        name,
                        email,
                        phone,
                        course,
                        status,
                        st.session_state.edit_id
                    )
                )
                conn.commit()
                st.success("Information successfully updated.")
        with col2:
            if st.button("⬅️ Back"):
                st.session_state.page = "search"
                st.rerun()               
def export_pdf():
    cursor.execute("SELECT id,student_id,name,email,phone,course,status FROM students")
    data=cursor.fetchall()
    table_data=[["ID","STUDENT_ID","NAME","EMAIL","PHONE","COURSE","STATUS"]] 
    for row in data:
        table_data.append(list(row))
    pdf=SimpleDocTemplate("students_report.pdf")
    table=Table(table_data)
    pdf.build([table])    
page()