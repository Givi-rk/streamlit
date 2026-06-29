import streamlit as st
from db import connection
from quiz import quiz_page
import pandas as pd
def dashboard():
    conn,cursor=connection()
    left,right=st.columns([8,4])
    with left:
        keyword=st.text_input("Search",placeholder="🔍Search...")
        c1,c2,=st.columns([8,3])
        with c2:
            cursor.execute("SELECT * FROM quiz_results")
            records=cursor.fetchall()
            df=pd.DataFrame(
                records,columns=["Id","Name","Score","Total Questions","Percentage","Submitted at"]
            )
            st.download_button("📥 Export CSV",df.to_csv(index=False),"quiz_results.csv","text/csv",use_container_width=True)
        if keyword:
            with st.container(border=True):
                search=f"%{keyword}%"
                col1,col2,col3,col4,col5,col6,col7=st.columns([1,4,2,4,2,3,3])
                col1.markdown("**ID**")
                col2.markdown("**NAME**")
                col3.markdown("**SCORE**")
                col4.markdown("**TOTAL QUESTIONS**")
                col5.markdown("**PC %**")
                col6.markdown("**SUBMITTED AT**")
                col7.markdown("**🗑️Delete**")
                cursor.execute("SELECT * FROM quiz_results WHERE name like %s",(search,))
                record=cursor.fetchall()
                if record:
                    for data in record:
                        c1,c2,c3,c4,c5,c6,c7=st.columns([1,4,2,4,2,3,3])
                        c1.write(f"{data[0]}")
                        c2.write(f"{data[1]}")
                        c3.write(f"{data[2]}")
                        c4.write(f"{data[3]}")
                        c5.write(f"{data[4]}")
                        c6.write(f"{data[5]}")
                        with c7:
                            with st.popover("Delete",key=f"{data[0]}"):
                                st.warning(f"Are you sure you want to delete {data[1]}?")
                                if st.button("Yes",key=f"button_{data[0]}"):
                                    cursor.execute("DELETE FROM quiz_results WHERE id=%s",(data[0],))
                                    conn.commit()
                                    st.success("Deleted successfully")
                else:
                    st.warning("No results found")
        else:
            with st.container(border=True):
                col1,col2,col3,col4,col5,col6,col7=st.columns([1,4,2,4,2,3,3])
                col1.markdown("**ID**")
                col2.markdown("**NAME**")
                col3.markdown("**SCORE**")
                col4.markdown("**TOTAL QUESTIONS**")
                col5.markdown("**PC %**")
                col6.markdown("**SUBMITTED AT**")
                col7.markdown("**🗑️Delete**")
                cursor.execute("SELECT * FROM quiz_results ORDER BY submitted_at DESC")
                record=cursor.fetchall()
                if record:
                    for data in record:
                        c1,c2,c3,c4,c5,c6,c7=st.columns([1,4,2,4,2,3,3])
                        c1.write(f"{data[0]}")
                        c2.write(f"{data[1]}")
                        c3.write(f"{data[2]}")
                        c4.write(f"{data[3]}")
                        c5.write(f"{data[4]}")
                        c6.write(f"{data[5]}")
                        with c7:
                            with st.popover("Delete",key=f"{data[0]}"):
                                st.warning(f"Are you sure you want to delete {data[1]}?")
                                if st.button("Yes",key=f"button_{data[0]}"):
                                    cursor.execute("DELETE FROM quiz_results WHERE id=%s",(data[0],))
                                    conn.commit()
                                    st.success("Deleted successfully")
                                    st.rerun()
    with right:
        st.write("")
        st.write("")
        with st.container(border=True):
            cursor.execute("SELECT COUNT(*) FROM quiz_results")
            total=cursor.fetchone()[0]
            st.metric("Total Participation",total)
        if st.button("Take Quiz",use_container_width=True):
            st.session_state.page="quiz"
            st.rerun()
        with st.container(border=True):
            st.subheader("📊Leaderboard")
            st.markdown("**TOP 10**")
            left,right=st.columns(2)
            left.write("NAME")
            right.write("SCORE")
            cursor.execute("SELECT *  FROM quiz_results ORDER BY score DESC LIMIT 10")
            datas=cursor.fetchall()
            for data in datas:
                with left:
                    st.write(f"{data[1]}")
                with right:
                    st.write(f"{data[2]}")
def page():
    st.set_page_config(
        page_title="Quiz",
        layout="wide"
    )
    if "page"not in st.session_state:
        st.session_state.page="dashboard"
    if st.session_state.page=="dashboard":
        dashboard()
    if st.session_state.page =="quiz":
        quiz_page()

page()