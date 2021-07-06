# Zemoga Test Portfolio
To use the API first install the requirements
- pip install -r requirements.txt

Add the .env file with all the environments variables to the root of project, the .env file was send with in the email, for security reasons I did not add it with in the github project

Then run the app
- python app.py

You can test each endpoint at http://127.0.0.1:5000/

Endpoints:

| Method | URL | Description |
| --- | ----------- | ----- |
| GET | /portfolio | Returns the data of all the portfolios in the DB |
| GET | /portfolio/{id} | Return the data of a portfolio given its id | 
| POST | /portfolio | Creates a portfolio |
| PUT | /portfolio/{id} | Updates a portfolio given its id |
| DELETE | /portfolio/{id} | Deletes a portfolio given its id |
| GET | /tweets/{screen_name} | Returns the last five tweets of an user given his/her screen_name |

Made:
- API REST CRUD of Portfolio
- API to get last 5 tweets a user given its username

Not made:
- Unittest
- Front API
- Swagger Documentation
- Docker
- More error management

Hours spend: 14

Most of my experience in python is with the Django framework, this is my first time working with the Flask framework, so it took me most of the time to learn from zero everything I needed to know about Flask, although it is not hard, the learning process consumed me a lot of time. 
I know how to make unittest and integration test with pytest, how do documentation with Swagger and Redoc, how to do complex querys and a lot of other things, but in Django

I wanted to complete every task but the time got me, still I am happy to made the core of the app done in time, to made all the API services successfully, and with this applying the basics of Flask, adding a new tool to my experience

Thank You

Made by Oscar David Garcia Medina