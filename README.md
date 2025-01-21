you can setup thsi project in 2 ways 

**NOTE:- AFTER SETUP THE DATABASE AND BACKEND YOU NEED TO HIT THIS CURL curl --location --request POST 'http://127.0.0.1:5000/api/initialize' 
ITS WILL INITIALIZE THE DATABASE WITH SOME TEST DATA LIKE CATEGORIES, PRODUCTS, PRICING, STOCK, FORECASTING LOG, OPTIMIZED PRICE, USER, ROLE, USER PERMISSION, ROLE AND PERMISSION MAPPING**


1. using docker compose
2. without docker compose

1.using docker compose

```
docker compose build 
docker compose up
```

using this cmd all the services backend, frontend and mysql 

the frontend will be available on port http://127.0.0.1:3001 
the backend will be available on port http://127.0.0.1:5001 
the mysql will be available on port http://127.0.0.1:3307
my sql credentials are 
username: root
password: password
database: bcg-data-base


env variables are in .env file
backend:{
DATABASE_URL=mysql+pymysql://root:password@mysql-server:3306/bcg-data-base // container port 
JWT_SECRET_KEY=your-secret-key-here
}


you connect this db using mysql workbench or any other mysql client



2. without docker compose

first setup sql in local machine

then run the backend and frontend in local machine

for backend first set env variables in .env file
backend:{
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/bcg-data-base // local host port
JWT_SECRET_KEY=your-secret-key-here
}

cmd for backend:-
1. python -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. flask run --host=0.0.0.0 --port=5000
this will start the serving on http://127.0.0.1:5000

cmd for frontend:-
1. npm install --force
2. check src/config.js file and change the base url to http://127.0.0.1:5000
3. npm start

frontend will be available on http://127.0.0.1:3000





