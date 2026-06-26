import streamlit as st
import pandas as pd
import plotly.express as px
from db_connection import connection
import os
def teacher_page():
    conn,cursor=connection()
    st.subheader("📊Teacher Dashboard")
    st.divider()
    c1,c2=st.columns([8,3])
    with c1:
        with st.container(border=True):
            cursor.execute("SELECT subject,SUM(status='Pending')AS Pending ,SUM(status='Review') AS Review FROM assignments GROUP BY subject")
            datas=cursor.fetchall()
            print(datas)
            df=pd.DataFrame(datas,columns=["Subject",'Pending','Reviewed'])
            df['Pending']=df['Pending'].astype(int)
            df['Reviewed']=df['Reviewed'].astype(int)
            fig=px.bar(df,x="Subject",y=["Pending","Reviewed"],barmode="group",title="Assignment status by subject",labels={"value":"Number of Assignments","Subject":"Subject"})
            st.plotly_chart(fig,use_container_width=True)
    with c2:
        with st.container(border=True):
            cursor.execute("SELECT COUNT(*) FROM assignments")
            total=cursor.fetchone()[0]
            st.metric("Total Submission",total)
        with st.container(border=True):
            cursor.execute("SELECT COUNT(*) FROM assignments WHERE status='Review'")
            review=cursor.fetchone()[0]
            st.metric("Reviewed Assignments",review)
        with st.container(border=True):
            cursor.execute("SELECT COUNT(*) FROM assignments WHERE status='Pending'")
            pending=cursor.fetchone()[0]
            st.metric("Pending",pending)        
    keyword=st.text_input("Search",placeholder="🔍 Search student..")
    if keyword:
        search=f"%{keyword}%"
        cursor.execute("SELECT * FROM assignments WHERE roll_no LIKE %s OR name LIKE %s",(search,search,))
        record=cursor.fetchall()
        if record:
            columns=["ID","NAME","ROLL NUMBER","ASSIGNMENT TITLE","SUBJECT","FILE","SUBMISSION DATE","STATUS","REMARK"]
            df=pd.DataFrame(record,columns=columns)
            st.dataframe(df,hide_index=True)
            for data in record:
                with st.expander(f"{data[0]}-{data[3]}"):
                    st.write(f"{data[4]}")
                    if os.path.exists(data[5]):
                        with open(data[5],"rb") as file:
                            st.download_button("Download assignment",file,file_name=os.path.basename(data[5]),key=f"download_{data[0]}")
                    st.write(f"{data[6]}")
                    reviewed=st.toggle("Reviewed",value=(data[7]=="Review"),key=f"{data[0]}")
                    status="Review"if reviewed else "Pending"
                    remark=st.text_area("Teacher Remark",value=data[8] if data[8] else "",key=f"remark_{data[0]}")    
                    if st.button("Update",key=f"update_{data[0]}"):
                        cursor.execute("UPDATE assignments SET status=%s,teacher_remark=%s WHERE id=%s",(status,remark,data[0],))
                        conn.commit()
                        st.success("Updated successfully.")    
                        st.rerun()
        else:
            st.write("Student not found.")
    else:
        cursor.execute("SELECT * FROM assignments ORDER BY submission_date DESC")
        record=cursor.fetchall()
        columns=["ID","NAME","ROLL NUMBER","ASSIGNMENT TITLE","SUBJECT","FILE","SUBMISSION DATE","STATUS","REMARK"]
        df=pd.DataFrame(record,columns=columns)
        st.dataframe(df,hide_index=True)
        for data in record:
            with st.expander(f"{data[0]}-{data[3]}"):
                st.write(f"{data[4]}")
                if os.path.exists(data[5]):
                    with open(data[5],"rb") as file:
                        st.download_button("Download assignment",file,file_name=os.path.basename(data[5]),key=f"download_{data[0]}")
                st.write(f"{data[6]}")
                reviewed=st.toggle("Reviewed",value=(data[7]=="Review"),key=f"toggle_{data[0]}")
                status="Review"if reviewed else "Pending"
                remark=st.text_area("Teacher Remark",value=data[8] if data[8] else "",key=f"remark_{data[0]}")    
                if st.button("Update",key=f"update_{data[0]}"):
                    cursor.execute("UPDATE assignments SET status=%s,teacher_remark=%s WHERE id=%s",(status,remark,data[0],))
                    conn.commit()
                    st.success("Updated successfully.")    
                    st.rerun()
