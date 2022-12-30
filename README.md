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

