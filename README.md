
project Video Link :-  
```bash
https://www.awesomescreenshot.com/video/35764742?key=8d9e01d31fd678c7baffa3661995bd08
```

You can set up this project in two ways:

**NOTE: AFTER SETTING UP THE DATABASE AND BACKEND, YOU NEED TO RUN THIS CURL COMMAND:**

```bash
curl --location --request POST 'http://127.0.0.1:5001/api/initialize'
```

**This will initialize the database with some test data like categories, products, pricing, stock, forecasting log, optimized price, user, role, user permission, and role and permission mapping.**

1. **Using Docker Compose**

   ```bash
   docker compose build
   docker compose up
   ```

   Using this command, all the services (backend, frontend, and MySQL) will be started.

   - The frontend will be available at: [http://127.0.0.1:3001](http://127.0.0.1:3001)
   - The backend will be available at: [http://127.0.0.1:5001](http://127.0.0.1:5001)
   - MySQL will be available at: [http://127.0.0.1:3307](http://127.0.0.1:3307)

   MySQL credentials are:
   - Username: `root`
   - Password: `password`
   - Database: `bcg-data-base`

   Environment variables are in the `.env` file:
   ```plaintext
   backend: {
     DATABASE_URL=mysql+pymysql://root:password@mysql-server:3306/bcg-data-base // container port
     JWT_SECRET_KEY=your-secret-key-here
   }
   ```

   You can connect to this database using MySQL Workbench or any other MySQL client.

2. **Without Docker Compose**

   First, set up MySQL on your local machine, then run the backend and frontend locally.

   For the backend, first set environment variables in the `.env` file:
   ```plaintext
   backend: {
     DATABASE_URL=mysql+pymysql://root:password@localhost:3306/bcg-data-base // local host port
     JWT_SECRET_KEY=your-secret-key-here
   }
   ```

   Commands for the backend:
   1. `python -m venv venv`
   2. `source venv/bin/activate`
   3. `pip install -r requirements.txt`
   4. `flask run --host=0.0.0.0 --port=5000`

   This will start the server on [http://127.0.0.1:5000](http://127.0.0.1:5000).

   Commands for the frontend:
   1. `npm install --force`
   2. Check `src/config.js` file and change the base URL to `http://127.0.0.1:5000`
   3. `npm start`

   The frontend will be available at [http://127.0.0.1:3000](http://127.0.0.1:3000).

   

https://github.com/user-attachments/assets/a0ca782a-b82a-40ea-b739-69ff804d1101


