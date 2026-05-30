# Customer Support

This repository contains the "customer-support" application — an assignment project for BookLeaf. The app is a simple, practical example of a customer support system that demonstrates best practices for building, running, and testing a small web service.

## Table of Contents
- About
- Key Features
- Tech Stack
- Installation
- ERD
- Configuration
- Author Login
- Staff Login


## About

The Customer Support application provides a foundation for handling user inquiries, tracking tickets, etc. It is intended as a learning and evaluation project for BookLeaf.

## Key Features

- Create, read, update, and close support tickets
- Simple REST API for integration and testing
- Basic data validation and error handling
- Clear project structure for easy extensibility

## Tech Stack

- Language: (Python, JavaScript)
- Web framework: (Django, Vue)
- Data store: (SQLite/PostgreSQL)
- AI Agent: (LangChain/LangGraph)

## ERD

`
+--------------------+        +-----------------------------+        +-----------------------------+
|       User         | 1    * |            Book             | 1    * |           Ticket            |
|--------------------|--------|-----------------------------|--------|-----------------------------|
| id (PK)            |        | id (PK)                    |        | id (PK)                    |
| username           |        | author_id (FK -> User.id)  |        | query                      |
| email              |        | title                      |        | book_id (FK -> Book.id)    |
| ...                |        | isbn                       |        | status                     |
+--------------------+        | genre                      |        | response                   |
                              | pub_date                   |        +-----------------------------+
                              | status                     |
                              | mrp                        |
                              | copies_sold                |
                              | royality_earned            |
                              | royality_paid              |
                              | royality_pending           |
                              +-----------------------------+
`


## Installation

docker compose up --build -d

Update these steps to match the project's actual dependency manager and commands.

## Configuration

- Copy any example environment file if available (e.g., .env.example -> .env).
- Ensure required environment variables are set before running the app.

## Author Login
Login with author username by combining first as last name with _
Example - Sneha_Kulkarni
password - hellYeah2020

## Staff Login

Login with following credentials to resolve tickets (Open staff in seperate window).
- username: vikas@gmail.com
  password: hello2020
