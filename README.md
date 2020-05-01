# covidtracker

the goal of this project was to gain experience using Django and database structures and how they're hosted/managed within a network.
we decided to create a web application to detect where the most number of people are at any given moment using Google Map's API.
we wanted to incorporate as many tables and charts to create one central location for coronavirus information and statistics.


steps to load

download python 3.7.6

pip install venv

mkvirtualenv covidtracker (or any other name you'd like)

virtualenv .\scripts\activate (try under the next line if doesn't work)

pip install -r requirements.txt

clone into github proj: https://github.com/xzrderek/covidtracker.git

----in github repo ----

C://covidtracker python manage.py makemigrations

C://covidtracker python manage.py migrate

C://covidtracker do python manage.py runserver --insecure

should load now at http://127.0.0.1:8000/
