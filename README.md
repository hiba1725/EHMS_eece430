# EHMS_eece430
> Django based application for an E Healthcare Management System developped for university course.

## Overview
E Healthcare Management System with login, signup and registration. This project allows the user to signup/login as a 
patient or as a doctor, to register appointments online with a specific doctor, and have a online chat with them. 
<br/>
There is also a manager application that is accessed url direct accessing `<mainurl.com>/manager/`. The  manager can 
add, delete and edit patients, doctors and appointments; as well as gets a monthly report.

## Requirements
To be able to run the Django server, you need to have the following tools on your machine
```
* Python 3.7+
* Django 3.1.6+
```
There are a number of packages to install. You can do that by running:
```
$ git clone https://github.com/KevinZiadeh/EHMS_eece430.git
$ cd EHMS_eece430/
$ pip install -r requirements.txt
```

## Run
To run this application, make sure to first be in the correct directtory in your terminal and have done the requirements. Then run:
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```
You should create a manager using the admin portal once.
To run the chat server, enter the command `python manage.py run_chat_server` from a seperate terminal after running `python manage.py runserver`
