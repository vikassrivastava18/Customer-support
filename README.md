# Customer Support

This repository contains the "customer-support" application — an assignment project for BookLeaf. The app is a simple, practical example of a customer support system that demonstrates best practices for building, running, and testing a small web service.

## Table of Contents
- About
- Key Features
- Tech Stack
- Installation
- ERD
- Configuration


## About

The Customer Support application provides a foundation for handling user inquiries, tracking tickets, and demonstrating basic API and UI patterns. It is intended as a learning and evaluation project for BookLeaf.

## Key Features

- Create, read, update, and close support tickets
- Simple REST API for integration and testing
- Basic data validation and error handling
- Clear project structure for easy extensibility

## Tech Stack

- Language: ( Python )
- Web framework: (Django)
- Data store: (SQLite/PostgreSQL)
- AI Agent: (LangChain/LangGraph)

## ERD

`
+--------------------+
|      User          |
|--------------------|
| id (PK)            |
| username           |
| email              |
| ...                |
+--------------------+
          |
          | 1
          |
          | *
+-----------------------------+
|            Book             |
|-----------------------------|
| id (PK)                    |
| author_id (FK -> User.id)  |
| title                      |
| isbn                       |
| genre                      |
| pub_date                   |
| status                     |
| mrp                        |
| copies_sold                |
| royality_earned            |
| royality_paid              |
| royality_pending           |
+-----------------------------+
          |
          | 1
          |
          | *
+-----------------------------+
|           Ticket            |
|-----------------------------|
| id (PK)                    |
| query                      |
| book_id (FK -> Book.id)    |
| status                     |
| response                   |
+-----------------------------+
`


## Installation

1. Clone the repository:

	unzip the folder

2. Install dependencies:
    cd frontend
	npm install
    npm run dev

3. Python installation:
    cd backend
	python -m venv venv
	source venv/bin/activate  # or venv\Scripts\activate on Windows
	pip install -r requirements.txt
    cd support
    python manage.py runserver

Update these steps to match the project's actual dependency manager and commands.

## Configuration

- Copy any example environment file if available (e.g., .env.example -> .env) and update settings such as database connection, ports, and secrets.
- Ensure required environment variables are set before running the app.

