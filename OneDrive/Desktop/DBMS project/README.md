# Event Management System - DBMS Project

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

A comprehensive full-stack application designed to showcase relational database concepts including normalization, constraints, triggers, stored procedures, and complex queries. 

## 📋 Entities Modeled
1. **Users** (Roles: Admin, Organizer, Attendee)
2. **Events**
3. **Venues**
4. **Registrations** (Many-to-Many resolution between Users and Events)
5. **Payments**
6. **Notifications**

## 📂 Project Structure
```text
├── backend/            # FastAPI Application, SQLAlchemy models, API endpoints
├── frontend/           # HTML, CSS, JavaScript files for the user interface
├── db/                 # Raw SQL scripts for DBMS requirements (MySQL, Oracle, Queries, Data)
├── scripts/            # Helper scripts (DB seeding, schema alterations)
├── .gitignore          # Git ignore configuration
└── event_management.db # Local SQLite Database
```

## 🚀 How to Run Locally

### 1. Database Setup
The backend is configured to use a local `SQLite` database (`event_management.db`) out-of-the-box so you can run the API immediately without installing an external database server.

If you wish to use MySQL or Oracle:
- Install your desired DBMS.
- Run the appropriate schema script from the `db/` folder (`schema_mysql.sql` or `schema_oracle.sql`).
- Update the connection string in `backend/database.py`.

### 2. Running the Backend
From the project root directory, install dependencies and start the application:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
The API will run at `http://127.0.0.1:8000`.
Visit [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs) to view the auto-generated Swagger UI Documentation.

### 3. Running the Frontend
Simply open `frontend/index.html` in your web browser, or serve it using a local HTTP server:
```bash
cd frontend
python -m http.server 3000
```
Then visit `http://localhost:3000`.

### 4. Helper Scripts
To seed your database with dummy data (Admin and Student accounts), you can use the script provided:
```bash
python scripts/seed_db.py
```
To run the database alteration testing script:
```bash
python scripts/alter.py
```

### 5. Required SQL Scripts & Queries
All explicit DBMS project requirements (Aggregate queries for participant count, SQL event registration, Views for event schedules) are fully documented in the `db/queries.sql` file.
