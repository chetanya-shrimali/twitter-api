# twitter-api
simple application that retrieves tweets from `Twitter API` based on search keywords, username and date.
The site is hosted at [https://twitter-api-project.herokuapp.com](https://twitter-api-project.herokuapp.com/)

### Installation (python 2.7)

- Get the requirements

`$ sudo apt-get install python-pip`

  
- Fork and clone the expenses-app repository

	`$ git clone https://github.com/<Username>/twitter-api`

- Now get the django specific requirements 
 	
	`$ cd expenses_app`
  
  	`$ pip install django`

- Now run the server 
 	
	`$ python manage.py runserver`

open [127.0.0.1:8000](127.0.0.1:8000) in the browser


- Apply the migrations(Already included for ease)

	`python manage.py makemigrations`

	`python manage.py migrate`

- Create the admin

	`python manage.py createsuperuser`

- Add the relevant information

- open [127.0.0.1:8000/admin](127.0.0.1:8000/admin)
