import streamlit as st
import pandas as pd
import plotly.express as px
if "page" not in st.session_state:
    st.session_state.page="dashboard"
# page config
def DashBoard():
    st.subheader("Dashboard Overview")
    col2A,col2B,col2C=st.columns([8,3,3])
    with col2A:
        st.write("Welcome back. Here is what is happening with your workforce today.")
    with col2B:
        if st.button("📥 Export CSV",use_container_width=True):
            st.success("Exported to CSV")
    with col2C:
        if st.button("+ Add Employees",use_container_width=True):
            st.session_state.page="add_employee"
    #row 1 columns
    col1,col2,col3,col4=st.columns(4,border=True)
    with col1:
        st.metric(
            "Total Employees","1,248","+12% this month"
    )
    with col2:
        st.metric("Active","1,102")
        st.caption("88.3 '%' of total workforce")
    with col3:
        st.metric("Pending Onboarding","94","12 starting next week")
    with col4:
        st.metric("Terminated","52")
        st.caption("YTD attrition rate: 4.1%")
    #growth chart
    # row 2 coulms
    colA,colB=st.columns([6,5],border=True)
    with colA:
        months=["Jan","Feb","Mar","Apr","May","Jun","July","Aug","Sep","Oct","Nov","Dec"]
        growth=[400,450,520,580,560,700,750,810,890,970,1010,1248]
        fig=px.bar(x=months,
                y=growth)
        st.plotly_chart(fig,use_container_width=True)
    # Department split
    with colB:
        st.subheader("Department Split")
        st.write("Engineering")
        st.progress(42)
        st.write("Product & Design")
        st.progress(21)
        st.write("Marketing")
        st.progress(15)
        st.write("Operations")
        st.progress(12)
        st.write("Support")
        st.progress(10)
        st.button("View All Departments",use_container_width=True)
    #4throw
    row41,row42=st.columns([4,6],border=True)
    with row41:
        st.subheader("Recent Activity")
        st.write("👤  Marcus Webb joined Engineering")
        st.caption("    2 hours ago")
        st.write("📈  Sarah Jenkins promoted to Lead Designer")
        st.caption("    5 hours ago")
        st.write("📝  David Chen Updated profile information")
        st.caption("    Yesterday")
        st.write("📴  Elena Rodrigues offboarding initiated")
        st.caption("    Oct 24,2023")
    #team member table
    with row42:
        mini_col1,mini_col2=st.columns([8,4])
        with mini_col1:
            st.subheader("Newest Team Members")
        with mini_col2:
            st.write("")
            st.button("View All Directory")
        df=pd.DataFrame({"EMPLOYEE":["Alex Rivera","Sophia Liang","James Wilson","Priya Patel"],"DEPARTMENT":["Engineering","Design","Marketing","Product"],
                        "START DATE":["Oct 26,2023","Oct 25,2023","Oct 24,2023","Oct 20,2023"],"STATUS":["Active","Pending","Active","Active"]})
        st.dataframe(df,width='stretch',hide_index=True)
#-----------------Employee directory------------------------------------
def Employee():
    st.subheader("Employee Directory")
    col1,col2,col3=st.columns([8,3,3])
    with col1:
        st.write("Manage and monitor 1,248 organization staff members.")
    with col2:
        if st.button("📥 Export CSV"):
            st.success("Exported to CSV")
    with col3:
        if st.button("+ Add Employees"):
            st.session_state.page="add_employee"
            st.rerun()
    with st.container(border=True):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 4, 3, 3, 2, 4])
        with col1:
            st.markdown("**Filter by:**")
        with col2:
            department = st.selectbox(
                "Department",
                ["All Departments", "Engineering", "Marketing",
                "Sales", "Finance", "Human Resources",],
                label_visibility="collapsed"
            )
        with col3:
            role = st.selectbox(
                "Role",
                ["All Roles", "Senior DevOps", "Brand Strategy",
                "Director of People", "Frontend Engineer"],
                label_visibility="collapsed"
            )
        with col4:
            st.button("🗑️ Bulk Delete")
        with col5:
            st.write("")
        with col6:
            st.caption("Showing 1–10 of 1,248")
    st.write("")
    with st.container(border=True):
        h1, h2, h3, h4, h5, h6 = st.columns([3, 2, 3, 2, 2, 2])

        h1.markdown("*Employee*")
        h2.markdown("*Department*")
        h3.markdown("*Role*")
        h4.markdown("*Status*")
        h5.markdown("*Last Active*")
        h6.markdown("*Action*")

        st.divider()

        # Data
        employees = [
            ["Elena Rodriguez", "Designer", "Senior Product Designer", "Active", "1 min ago"],
            ["Ricardo Mendoza", "Engineering", "Senior DevOps", "Active", "2 mins ago"],
            ["Elena Chen", "Marketing", "Brand Strategy Lead", "Active", "1 hour ago"],
            ["Marcus Holloway", "Human Resources", "Director of People", "Inactive", "3 days ago"],
            ["Sophie Mueller", "Engineering", "Frontend Engineer", "Active", "Just now"],
            ["Arjun Patel", "Sales", "Account Executive", "Active", "15 mins ago"]
        ]

        for i, emp in enumerate(employees):
            c1, c2, c3, c4, c5, c6 = st.columns([3, 2, 3, 2, 2, 2])

            c1.write(emp[0])
            c2.write(emp[1])
            c3.write(emp[2])
            c4.write(emp[3])
            c5.write(emp[4])

            if c6.button("View", key=f"view_{i}"):
                st.session_state.page="profile"
                st.rerun()

            st.divider()
        left,mid,right=st.columns([4,4,6])
        with left:
            st.write("showing 1 to 10 of 1,248 entries")
        with right:
            in1,in2,in3,in4,in5,in6=st.columns([2,2,2,2,3,2])
            with in1:
                st.button("<", key='a')
            with in2:
                st.button("1",key='b')
            with in3:
                st.button("2",key='c')
            with in4:
                st.button("..",key='d')
            with in5:
                st.button("12",key='e')
            with in6:
                st.button(">",key='f')
    st.write("")
    c1,c2,c3=st.columns(3,border=True)
    with c1:
        st.subheader("Hiring Velocity")
        st.caption("Your organistaion grew by 14% this quarter.")
        st.button("View Report")
    with c2:
        st.subheader("Team Sync")
        st.caption("Next organisation sync in 3 hours.")
    with c3:
        st.header("System Health")
        st.caption("All HR integrations are currently operational.")
        st.write("✅ Sync: 100'%' stable")
#-------add employess-------
def add_employee():
    if st.button("⬅️ Back to Employee List"):
        st.session_state.page="employees"
        st.rerun()
    st.subheader("Create New Employee")
    st.caption("Onboard a new member to the enterprise system.")
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.write("1️⃣")
        st.caption("Personal Info")
    with c2:
        st.write("2️⃣")
        st.caption("Job Details")
    with c3:
        st.write("3️⃣")
        st.caption("Compensation")
    with c4:
        st.write("4️⃣")
        st.caption("Review")
    with st.container():
        st.subheader("Basic Identity")
        st.write("Enter the legal name and contact details")
        upload_file=st.file_uploader("Upload Photo",type=["jpg","png","jpeg"])
    col1,col2=st.columns(2)
    with col1:
        first_name=st.text_input("First Name")
    with col2:
        last_name=st.text_input("Last Name")
    col3,col4=st.columns(2)
    with col3:
        email=st.text_input("Email Address")
    with col4:
        dob=st.date_input("Date of Birth",value=None)
    Address=st.text_input("Residential Address")
    st.divider()
    b1,b2,b3=st.columns([2,6,2])
    with b1:
        if st.button("💾 Save Draft"):
            st.info("saved to draft")
    with b3:
        st.button("Next", type="primary",use_container_width=True)
def profile():
    col1,col2=st.columns([4,10])
    with col1:
        st.caption("Employee > Profile Views")
    with st.container(border=True):
        col3,col4,col5=st.columns([3,6,3])
        with col3:
            st.write("")
            st.image("https://cdn-icons-png.flaticon.com/128/1144/1144760.png")
        with col4:
            st.subheader("Elena Rodrigues","Emp ID:#SP-8842")
            st.caption("Senior Product Designer")
            c1,c2=st.columns(2)
            with c1:
                st.write("🏬 Product & Design")
            with c2:
                st.write("📍 Austin,TX(Remote)")
            st.write("🗓️ Joined June 15,2021")
        with col5:
            st.write("")
            st.button("✏️ Edit Profile ")
            st.button("✉️ Send Message")
    tab1,tab2,tab3,tab4,tab5=st.tabs(["Overview","Employment","Payroll","Documents","Activity"])
    with tab1:
        left,right=st.columns([4,3])
        with left:
            with st.container(border=True):
                st.subheader("👤 Personal Info")
                st.divider()
                c3,c4=st.columns(2)
                with c3:
                    st.caption("LEGAL NAME")
                    st.markdown("**Elena Mercedes Rodriguez**")
                    st.caption("PHONE NUMBER")
                    st.markdown("**+1 (512) 445-9032**")
                    st.caption("HOME ADDRESS")
                    st.markdown("**4220 Oakwood Trail,Austin,TX 78741**")
                with c4:
                    st.caption("EMAIL ADDRESS")
                    st.markdown("**e.rodriguez@staffportal.com**")
                    st.caption("DATE OF BIRTH")
                    st.markdown("**March 12,1992**")
                    st.caption("EMERGENCY CONTACT")
                    st.markdown("**Marcus Rodriguez(Brother)-512-555-0199**")
            with st.container(border=True):
                st.subheader("🕘Career Timeline")
                st.divider()
                r1,r2=st.columns([1,3])
                with r1:
                    st.write("📈")
                with r2:
                    st.markdown("**Jan 2024-Present**")
                    st.write("Promoted to Senior Product Designer")
                    st.caption("Advanced to senior level after successful delivery of the Enterprise Design System project.")
                r3,r4=st.columns([1,3])
                with r3:
                    st.write("↔️")
                with r4:
                    st.markdown("**Aug 2022**")
                    st.write("Department Transfer: Product & Design")
                    st.caption("Transfer from Creative Marketing to Core Product team to focus on application UX.")
                r5,r6=st.columns([1,3])
                with r5:
                    st.write("📲")
                with r6:
                    st.markdown("**Jun 2021**")
                    st.write("Joined as Associate Designer")
                    st.caption("Hired through the National Talent Program for the Austin headquarters.")
        with right:
            with st.container(border=True):
                st.subheader("Organisation Heirarchy")
                st.write("REPORTS TO")
                with st.container(border=True):
                    lef,mid=st.columns([1,2])
                    with lef:
                        st.write("")
                        st.write("")
                        st.write("👨🏻‍💻")
                    with mid:
                        st.markdown("**David Chen**")
                        st.write("VP of Product >")
                        st.write("Design")
                st.write("DIRECT REPORTS (0)")
                with st.container(border=True):
                    left,mid,right=st.columns([1,2,1])
                    with mid:
                        st.write("Individual Contributor")
                st.write("TEAM MEMBERS")
                st.write("👷🏻‍♀️👩🏻‍🎓👩🏻‍💻👩🏻‍💻👷🏼 +12")
            with st.container(border=True):
                st.subheader("Skills & Competencies")
                left,right=st.columns(2)
                with left:
                    st.button("UX",use_container_width=True)
                    st.button("Prototyping",use_container_width=True)
                    st.button("Accessibility",use_container_width=True)
                with right:
                    st.button("Design",use_container_width=True)
                    st.button("User",use_container_width=True)
                    st.button("Figma",use_container_width=True)
            with st.container(border=True):
                st.subheader("Admin Actions")
                st.button("📃 Review Performance",use_container_width=True)
                st.button("👝 Adjust Salary",use_container_width=True)
                st.button("📴 Offboarding Flow",use_container_width=True)
            
def page():
    st.set_page_config(
        page_title="StaffPortal",
        page_icon="💼",
        layout="wide"
    )
    #sidebar

    col1A,col1B,col1C,col1D=st.columns([8,1,1,1])
    col1A.text_input("",placeholder="🔍 Search employees,documents...")
    with col1B:
        st.write("")
        st.write("")
        st.button("🔔")
    with col1C:
        st.write("")
        st.write("")
        st.button("❓")
    with col1D:
        st.write("")
        st.write("")
        st.button("👩‍💼")
    with st.sidebar:
        st.sidebar.title("StaffPortal")
        st.sidebar.caption("Enterprise HRMS")
        if st.button("Dashboard",use_container_width=True):
            st.session_state.page="dashboard"
        if st.button("Employees",use_container_width=True):
            st.session_state.page="employees"
        if st.button("Roles",use_container_width=True):
            st.session_state.page="roles"
        if st.button("Departments",use_container_width=True):
            st.session_state.page="departments"
        if st.button("Reports",use_container_width=True):
            st.session_state.page="reports"
        if st.button("Settings",use_container_width=True):
            st.session_state.page="settings"
        st.write("**John Doe**")
        st.caption("HR DIRECTOR")
    if st.session_state.page=="dashboard":
        DashBoard() 
    elif st.session_state.page=="employees":
        Employee()
    elif st.session_state.page=="roles":
        st.title("Roles")
    elif st.session_state.page=="departments":
        st.title("Departments")
    elif st.session_state.page=="reports":
        st.title("Reports")
    elif st.session_state.page=="settings":
        st.title("Settings")
    elif st.session_state.page=="add_employee":
        add_employee()
    elif st.session_state.page=="profile":
        profile()
page()