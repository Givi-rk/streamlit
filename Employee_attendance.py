import mysql.connector
import streamlit as st
import pandas as pd
from datetime import date, datetime
import plotly.express as px
if "page" not in st.session_state:
    st.session_state.page="dashboard"
try:
    conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='attendance_db'
    )
    cursor=conn.cursor()
except mysql.connector.Error as e:
    st.error("Error:",e)
def add_attendance():
    st.subheader("Add Attendance")
    with st.form("Attendance Form"):
        emp_id=st.text_input("Employee Id")
        emp_name=st.text_input("Employee Name")
        dept=st.selectbox("Department",["IT","MARKETING","HR","FINANCE","SALES"])
        att_date=st.date_input("Attendance Date",value=date.today())
        status=st.radio("status",["Present","Absent","Leave","Half Day"])
        if st.form_submit_button("➕ Add Attendance"):
            cursor.execute("INSERT INTO attendance (employee_id,employee_name,department,attendance_date,status) VALUES(%s,%s,%s,%s,%s)",(emp_id,emp_name,dept,att_date,status))
            conn.commit()
            st.success("Attendance added successfully.")
def search_update():
    keyword=st.text_input("Search",placeholder="🔍 Search Employee...")
    search=f"%{keyword}%"
    if keyword:
        cursor.execute("SELECT * FROM attendance WHERE employee_id LIKE %s OR employee_name LIKE %s OR department LIKE %s",(search,search,search,))
        st.session_state.search_results=cursor.fetchall()
        if "search_results" in st.session_state:
            data=st.session_state.search_results
            with st.container(border=True):
                c1,c2,c3,c4,c5=st.columns([2,3,3,2,1])
                with c1:
                    st.markdown("**Employee Id**")
                with c2:
                    st.markdown("**Name**")
                with c3:
                    st.markdown("**Department**")
                with c4:
                    st.markdown("**Status**")
                with c5:
                    st.markdown("**View**")
                if data:
                    for record in data:
                        col1,col2,col3,col4,col5=st.columns([2,3,3,2,1])
                        with col1:
                            st.write(record[1])
                        with col2:
                            st.write(record[2])
                        with col3:
                            st.write(record[3])
                        with col4:
                            st.write(record[5])
                        if col5.button("✏️Edit",key=str(record[0])):
                            print('Setting....')
                            st.session_state.selected_employee=record
                            st.session_state.page = "details"
                            st.rerun()
                else:
                    st.error("Employee not found.")
def employee_details():
    record=st.session_state.selected_employee
    if st.button("⬅️ Back"):
        st.session_state.page="search"
        st.rerun()
    st.subheader("Employee Details")
    st.write("Employee Id:",record[1])
    emp_name=st.text_input("Employee Name",value=record[2])
    departments=["IT","MARKETING","HR","FINANCE","SALES"]
    dept=st.selectbox("Department",departments,departments.index(record[3]))
    att_date=st.date_input("Attendance Date",value=record[4])
    status=st.radio("status",["Present","Absent","Leave","Half Day"],index=["Present","Absent","Leave","Half Day"].index(record[5]))
    col1,col2=st.columns(2)
    with col1:
        if st.button("Update"):
            cursor.execute("UPDATE attendance SET employee_name=%s,department=%s,attendance_date=%s,status=%s WHERE employee_id=%s",(emp_name,dept,att_date,status,record[1]))
            conn.commit()
            st.success("Updated Successfully")
    with col2:
        with st.popover("Delete"):
            st.warning("Are you sure you want to delete this employee?")
            if st.button("Yes,Delete"):
                cursor.execute("DELETE FROM attendance WHERE id=%s",(record[0],))
                conn.commit()
                st.success("Employee deleted successfully.")
                del st.session_state.selected_employee
                st.session_state.page="search"
                st.session_state.confirm_delete=False
                st.rerun()
def view():
    st.subheader("Employee Directory")
    col2A,col2B,col2C=st.columns([8,3,3])
    with col2A:
        st.write("Welcome back.")
    with col2B:
        cursor.execute("SELECT * FROM attendance")
        data=cursor.fetchall()
        df=pd.DataFrame(data,columns=["ID","Empoyee Id","Name","Department","Attendance Date","Status","Created at"])
        csv=df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Export CSV",csv,"attendance_records.csv",
                           "text/csv",use_container_width=True)
    with col2C:
        if st.button("+ Add Employees",use_container_width=True):
            st.session_state.page="add"
            st.rerun()
    cursor.execute("SELECT * FROM attendance ORDER BY attendance_date DESC")
    data=cursor.fetchall()
    df=pd.DataFrame(data,columns=["ID","EMPLOYEE ID","NAME","DEPARTMENT","DATE","STATUS","CREATED AT"])
    st.table(df)
def dashboard():
    st.subheader("DashBoard")
    col2A,col2B,col2C=st.columns([8,3,3])
    with col2A:
        st.write("Welcome back.Here what is happening with our workforce today.")
    with col2C:
        if st.button("+ Add Employees",use_container_width=True):
            st.session_state.page="add"
            st.rerun()
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status='Absent'")
    absent=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status='Leave'")
    leave=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status='Half Day'")
    half=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) AS today FROM attendance WHERE attendance_date=CURDATE()")
    today=cursor.fetchone()[0]
    c1,c2,c3=st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**👥 TOTAL ATTENDANCE**")
            st.write(f"{total}")
    with c2:
        with st.container(border=True):
            st.markdown("**👨🏽‍💻Present**")
            st.write(f"{present}")
    with c3:
        with st.container(border=True):
            st.markdown("**🆎Absent**")
            st.write(f"{absent}")
    c4,c5,c6=st.columns(3)
    with c4:
        with st.container(border=True):
            st.markdown("**➖On Leave**")
            st.write(f"{leave}")
    with c5:
        with st.container(border=True):
            st.markdown("**Half Day**")
            st.write(f"{half}")
    with c6:
        with st.container(border=True):
            st.markdown("**Today's Attendance**")
            st.write(f"{today}")

    left,right=st.columns(2)
    with left:
        with st.container(border=True):
            cursor.execute("SELECT status,COUNT(*) as total FROM attendance GROUP BY status")
            data=cursor.fetchall()
            df=pd.DataFrame(data,columns=["status","total"])
            fig=px.pie(df,names="status",values="total",title="Attendance Distribution")
            st.plotly_chart(fig)
    with right:
        with st.container(border=True):
            st.subheader("Department-wise Attendance Count")
            cursor.execute("SELECT department,COUNT(*) as total FROM attendance GROUP BY department")
            data1=cursor.fetchall()
            df=pd.DataFrame(data1,columns=["department","total"])
            fig=px.bar(df,x="department",y="total",title="Department-wise Attendance Count",labels={"department":"Department","total":"Attendance Records"})
            st.plotly_chart(fig,use_container_width=True)
def page():
    st.set_page_config(
        page_title="Employee Attendance",
        layout="wide"
    )
    u1,u2,u3,u4=st.columns([8,1,1,2])
    with u1:
        st.text_input("Search",value="🔍 search....")
    with u2:
        st.write("")
        st.write("")
        st.button("🔔",use_container_width=True)
    with u3:
        st.write("")
        st.write("")
        st.button("❓",use_container_width=True)
    with u4:
        st.write("")
        st.write("")
        st.button("👷🏻‍♀️")
    st.divider()
    with st.sidebar:
        st.sidebar.title("StaffPortal")
        if st.button("📊Dashboard",use_container_width=True):
            st.session_state.page="dashboard"
        if st.button("➕Add Attendance",use_container_width=True):
            st.session_state.page="add"
        if st.button("👥View Employees",use_container_width=True):
            st.session_state.page="employees"
        if st.button("🔍Search",use_container_width=True):
            st.session_state.page="search"
        if st.button("⚙️Settings",use_container_width=True):
            st.session_state.page="settings"
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("ADMIN")
        st.caption("EMP-#000")
    if st.session_state.page=="dashboard":
        dashboard() 
    elif st.session_state.page=="employees":
        view()
    elif st.session_state.page=="search":
        search_update()
    elif st.session_state.page=="settings":
        st.title("Settings")
    elif st.session_state.page=="add":
        add_attendance()
    elif st.session_state.page=="details":
        employee_details()

#st.session_state.selected_employee = (0, "emp-id", "nma", "dept", date.today(), 'Present', '')
page()