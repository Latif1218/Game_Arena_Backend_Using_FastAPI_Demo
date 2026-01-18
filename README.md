# Game Arena Backend Using FastAPI 

**Game Arena Backend Using FastAPI Demo** is a backend API project built with **Python** and **FastAPI**.  
This demo project demonstrates how to structure and build a game-related backend API using FastAPI, including database migrations and app configuration.

---

## 📁 Repository Structure

```

GameArena_Backend/
├── alembic/                        # Database migrations (Alembic)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                   # migration files
│
├── app/
│   ├── init.py
│   │
│   ├── Authentication/             # auth logic + jwt / password handling
│   │   ├── init.py
│   │   └── user_auth.py
│   │
│   ├── Match_helper/               # matchmaking business logic
│   │   ├── init.py
│   │   └── match_helper.py
│   │
│   ├── Wallet_helper/              # wallet, balance, transaction logic
│   │   ├── init.py
│   │   └── wallet_helper.py
│   │
│   ├── models/                     # SQLAlchemy ORM models
│   │   ├── init.py
│   │   ├── _match_models.py
│   │   ├── user_match_model.py
│   │   ├── user_models.py
│   │   ├── user_participant_model.py
│   │   ├── user_transaction_models.py
│   │   └── user_wallet_models.py
│   │
│   ├── routes/                     # API endpoints (routers)
│   │   ├── init.py
│   │   ├── admin.py
│   │   ├── forgot.py               # password reset?
│   │   ├── matches.py
│   │   ├── register_user.py
│   │   ├── user.py
│   │   └── wallet.py
│   │
│   └── schemas/                    # Pydantic models (request/response)
│       ├── init.py
│       ├── user_match_schemas.py
│       ├── user_schemas.py
│       ├── user_transaction_schemas.py
│       └── user_wallet_schemas.py
│
├── utils/
│   ├── init.py
│   ├── config.py                   # settings, env variables
│   └── database.py                 # engine, session, get_db dependency
│
├── .gitignore
├── alembic.ini
├── config.py                       # (sometimes placed in root)
├── database.py                     # (sometimes placed in root)
├── main.py                         # FastAPI app entry point
├── requirements.txt
├── LICENSE
└── README.md

````

---

## 🚀 About FastAPI

**FastAPI** is a modern Python web framework for building high-performance APIs with automatic documentation support.  
It uses Python type hints to simplify development and generate interactive API docs. ([fastapi.tiangolo.com](https://fastapi.tiangolo.com))

---

## 🧠 Project Overview

This repository demonstrates:

- Building REST APIs using FastAPI
- Database migrations using **Alembic**
- Organized project structure with modular code
- API endpoints for game arena operations (depending on `app/` code)

It serves as a demo backend for game-related services.

---

## 🧪 Prerequisites

Before running the project, make sure you have:

- Python 3.8 or above installed
- Virtual environment setup (optional but recommended)

---

## ⚙️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Latif1218/Game_Arena_Backend_Using_FastAPI_Demo.git
````

2. **Go to the project directory:**

```bash
cd Game_Arena_Backend_Using_FastAPI_Demo
```

3. **Create and activate a virtual environment (optional):**

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

4. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

Once dependencies are installed, start the FastAPI server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

* `app.main:app` tells Uvicorn where your FastAPI application instance is located.
* `--reload` enables auto-reload during development.

Your API will be available at:

```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

FastAPI provides automatic interactive documentation:

* **Swagger UI**

```
http://127.0.0.1:8000/docs
```

* **ReDoc**

```
http://127.0.0.1:8000/redoc
```

These pages allow you to explore and test API endpoints without a frontend client.

---

## 🛠️ Database Migrations (Alembic)

This project uses **Alembic** for managing database schema changes.

Basic Alembic workflow:

* Generate a new migration:

```bash
alembic revision --autogenerate -m "Your message"
```

* Apply migrations:

```bash
alembic upgrade head
```

Make sure your database connection is configured properly in the Alembic config.

---

## 📦 Requirements

All Python dependencies are listed in `requirements.txt`.
Common libraries include:

```
fastapi
uvicorn
alembic
sqlalchemy
...
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 📜 License

This project is licensed under the **MIT License**.
You are free to use, modify, and share the code according to the license terms.

---

## 🤝 Contribution

Contributions are welcome!
To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

---

## ⭐ Acknowledgements

Thank you for checking out this FastAPI demo backend project!
Happy coding and best of luck building your game APIs! 🚀

```bash
https://github.com/Latif1218/Fastapi_Project_1.git
```
