# DjangoTutorial

Check version : python -m django --version

Creating Project:
1.mkdir djangotutorial
2.django-admin startproject mysite djangotutorial

Run Server : python manage.py runserver

To create poll : python manage.py startapp polls

Unapplied migrations : python manage.py migrate


When U run at localhost 
Django does not allow post requests at local host 
To avoid it use @csrf_exempt cookie ....For this set environment in powershell:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate


also to import  @csrf_exempt cookie use from django.views.decorators.csrf import csrf_exempt


Sqllite 3 

python manage.py dbshell (For database)
PRAGMA table_info(polls_post);


.tables

