# Assignment Management System
A simple Assignment Management System built using Python, Streamlit, and MySQL. It allows students to submit assignments online and enables teachers to review, manage, and provide feedback through an interactive dashboard.
## Installation
```
pip install -r requirements.txt
```
## Database Setup
- Install [XAMPP](https://www.apachefriends.org/)acoording to your os.
- Make sure MySQL and Apache server is up and ruuning in the XAMPP control panel.
- Next, open [PHP MY ADMIN](http://localhost/phpmyadmin/) and go to SQL to run the following commands:
![Creation](./images/creation.png)
- Next, you can proceed to run the app.
## Running the Project
```
streamlit run main.py
```
## Database Screenshot
![Database](./images/db.png)
## Project Screenshot
### [Log in Page](main.py)
![Home](./images/login.png)
### [Student Page](student.py)
![Student](./images/submit.png)
![Student_success](./images/submit_success.png)
### [Teacher Page](teacher.py)
![Dashboard](./images/dashboard_1.png)
![Update](./images/dashboard_update.png)
![Search](./images/dashboard_search.png)