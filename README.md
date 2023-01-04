# FastAPI-project

In order to be able to run the following project you have to do
1) create virtual environment
go to the folder where you want to create virtual environment then run
> python -m venv env
instead of env you can write whatever you want

2) activate virtual environment
for mac OS
> env/bin/activate
for windows
> env\Scripts\activate

3) install all the required packages by runnig the following command
> pip install -r requirements.txt

4) and the last one, you have to run the server locally
> uvicorn megafon_users.main:app --reload

5) to check the api, go to the 
http://localhost:8000/docs
here you can find all availabe api for this project

# Translations of some important words to Russian
1) Subscription - Тариф
2) Service - Услуга
3) User - Пользователь

# how to use endpoint
# now the database is empty, so in order to work with endpoints you should add some data to that

We have POST, PUT, GET, DELETE methods
as the name defines POST-for creating, GET-for retrieving, PUT-for updating, DELETE-for deleting




