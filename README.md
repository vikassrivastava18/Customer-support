# Customer Support

Get quick support for authors published books, submit service requests, and explore frequently asked questions about the publishing process, royalties, etc.
Instant agentic chat to anwer all your queries

<img src="assets/support_graph.png" alt="LangGraph workflowdiagram" width="500"/>

## LangGraph Workflow Diagram
<img src="assets/screenshot.png" alt="Home Page" width="500"/>


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

```

+--------------------+        +-----------------------------+        +-----------------------------+
|       User         | 1    * |            Book             | 1    * |           Ticket            |
|--------------------|--------|-----------------------------|--------|-----------------------------|
| id (PK)            |        | id (PK)                     |        | id (PK)                     |
| username           |        | author_id (FK -> User.id)   |        | query                       |
| email              |        | title                       |        | book_id (FK -> Book.id)     |
| ...                |        | isbn                        |        | status                      |
+--------------------+        | genre                       |        | response                    |
                              | pub_date                    |        +-----------------------------+                            
                              +-----------------------------+                          
                              
```


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
