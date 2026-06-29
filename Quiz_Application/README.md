# Quiz Application 
a simple Quiz Application built using Python, Streamlit, and MySQL. Users can take a timed multiple-choice quiz, view their score and percentage, and have their results stored in a MySQL database. The application also provides a dashboard for viewing previous quiz attempts, searching results, exporting data to CSV, and displaying a leaderboard.
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
![Database](./images/database.png)
## Project Screenshot
### [DashBoard](app.py)
![Home](./images/dashboard.png)
### [Start Page](quiz.py)
![Student](./images/start_page.png)
![Demo Q1](./images/quiz_time.png)
![Demo Q2](./images/quiz_time2.png)
![Success](./images/quiz_completion.png)
### [Search](app.py)
![Search1](./images/search1.png)
![Search2](./images/search.png)
### Delete
![Delete](./images/delete.png)
### A sample of the [CSV](./images/quiz_results.csv) file.