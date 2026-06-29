import streamlit as st
import random
from db import connection
import time
from questions import total_questions
def quiz_page():
    conn,cursor=connection()
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started=False
    if not st.session_state.quiz_started:
        st.markdown("<h1 style='text-align:center'>Quiz Application</h1>",unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center'>Ready for a fun harry potter Quiz?</h3>",unsafe_allow_html=True)
        st.markdown("<h4 style='text-align:center'>Click the button below to start👇🏻.<br>Good Luck😊</h4>",unsafe_allow_html=True)
        left,mid,right=st.columns(3)
        with mid:
            name=st.text_input("Enter your name",placeholder='e.g. Givi')
            if st.button("Start"):
                if not name:
                    st.warning("Please enter your name")
                    return
                questions=total_questions()
                random.shuffle(questions)
                for q in questions:
                    random.shuffle(q["options"])
                st.session_state.name=name
                st.session_state.questions=questions
                st.session_state.current=0
                st.session_state.score=0
                st.session_state.start=time.time()
                st.session_state.quiz_started=True
                st.rerun()
            return
    if "result_saved" not in st.session_state:
        st.session_state.result_saved=False
    if st.session_state.current>=len(st.session_state.questions):
        total=len(st.session_state.questions)
        score=st.session_state.score
        percentage=round(score/total *100,2)
        if not st.session_state.result_saved:
            cursor.execute("INSERT INTO quiz_results(name,score,total_questions,percentage)VALUES(%s,%s,%s,%s)",(st.session_state.name,score,total,percentage,))
            conn.commit()
            st.session_state.result_saved=True
        st.success("Good job! you have completed the Quiz ")
        st.markdown(f"<h3>Score:{score}/{total}</h3>",unsafe_allow_html=True)
        st.write(f"<h3>Percentage:{percentage}%<h3>",unsafe_allow_html=True)
        if st.button("📊Back to Dashboard"):
            keys=["quiz_started","questions","current","score","start","name"]
            for key in keys:
                del st.session_state[key]
            st.session_state.page="dashboard"
        return
    c1,c2,c3=st.columns(3)
    with c2:
        with st.container(border=True):
            question=st.session_state.questions[st.session_state.current]
            elapsed=int(time.time()-st.session_state.start)
            remaining=30-elapsed
            if remaining<=0:
                st.warning("Time Up!")
                st.session_state.current+=1
                st.session_state.start=time.time()
                st.rerun()
            st.title("📑Quiz")
            st.progress(remaining/30)
            st.write(f"⏱️Time Left:{remaining} sec")
            st.subheader(f"Question {st.session_state.current+1}/{len(st.session_state.questions)}")
            st.write(question["question"])
            answer=st.radio("Select one",question["options"],key=st.session_state.current)
            if st.button("Next"):
                if answer==question["answer"]:
                    st.session_state.score+=1
                st.session_state.current+=1
                st.session_state.start=time.time()
                st.rerun()
            time.sleep(1)