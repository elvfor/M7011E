# M7011E
This is for a project in course M7011E. 

### Authors
**Jenny Sundström, Elvira Forslund Widenroth and Peggy Khialie**

ejyuso-2@student.ltu.se 

elvfor-0@student.ltu.se 

pegkhi-0@student.ltu.se

Our chosen project for the course is a Task Manager.


## Preparations

- Clone the git repo.

- Set up a virtual environment 

- Set up a SQLite database and use following commands:
  
run python manage.py migrate

run python manage.py makemigrations

- Install the requirements listed in the requirements.txt file with command:
run pip install -r requirements.txt

- Create a super user with:
run python manage.py createsuperuser 

## Groups

When you can access the admin page the following groups and permissions needs to be created in order for the system to work as intended:

#### Organization Leader:
- Can change and view organization
- Can add and delete projects


#### Project leader
- Can view, add, change and delete projects
- Can view, add, change and delete tasks


#### Worker
- Can view, add, change and delete tasks

- ## Running the code

Stand in M7011E/dev/TaskManager and run command:

python manage.py runserver

## Evaluation of performance
See dev/TaskManaggger/main/performance_documentation.MD for documentation of the performance + more. 







