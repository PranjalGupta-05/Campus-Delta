# SmartCampus AI

### An LLM-Driven University Information System

SmartCampus AI is a full-stack web application designed to provide students with a centralized conversational interface for accessing university information and submitting administrative complaints.

The system combines a responsive Single Page Application (SPA), a FastAPI backend, a MySQL relational database, and the Google Gemini Large Language Model. It uses a localized Retrieval-Augmented Generation (RAG) approach to provide institution-specific information through database-backed context.

## Overview

University information is often distributed across different platforms, making it difficult for students to access routine information such as faculty details, facility information, and mess schedules.

SmartCampus AI addresses this problem through a unified conversational interface that allows students to interact with campus information using natural language.

The system also provides a simplified mechanism for submitting complaints directly through the chat interface.

## Key Features

* Conversational interface for university-related queries
* Faculty information retrieval
* Mess and menu information
* Localized Retrieval-Augmented Generation (RAG)
* Google Gemini integration
* Student complaint submission
* User registration and login
* Bcrypt-based password hashing
* Content moderation using `better-profanity`
* MySQL-based institutional data storage
* Responsive Single Page Application

## Architecture

The application follows a client-server architecture:

```text
┌──────────────────────┐
│        Student       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Frontend (SPA)    │
│ HTML5 / CSS3 / JS    │
└──────────┬───────────┘
           │
           │ Fetch API
           ▼
┌──────────────────────┐
│    FastAPI Backend   │
│       Python         │
└──────────┬───────────┘
           │
      ┌────┴─────┐
      │          │
      ▼          ▼
┌──────────┐  ┌──────────────┐
│  MySQL   │  │ Google Gemini│
│ Database │  │     LLM      │
└──────────┘  └──────────────┘
```

For supported campus-related queries, the backend retrieves relevant information from the MySQL database and provides it as context to the Gemini model.

## Localized RAG

SmartCampus AI uses a lightweight, localized RAG approach based on the MySQL relational database.

Instead of using a separate vector database, the backend retrieves relevant tabular information using keyword-based triggers and injects the retrieved data into the LLM prompt.

For example:

* Queries containing terms such as `teach`, `faculty`, or `professor` can retrieve faculty information.
* Queries containing terms such as `mess`, `menu`, or `food` can retrieve the weekly mess schedule.

The retrieved information is then used as context when generating the response through Gemini.

## Complaint Handling

Complaint submission uses a separate processing path from normal AI queries.

A complaint can be submitted using the following format:

```text
complaint: <complaint description>
```

Example:

```text
complaint: The fan in room 204 is not working.
```

When the `complaint:` prefix is detected, the request bypasses the generative AI pipeline.

The complaint is directly inserted into the MySQL complaints table with:

* Complaint ID
* Complaint description
* `Open` status
* Date and time

A confirmation containing the generated complaint ID is then returned to the user.

## Authentication and Moderation

The system includes user registration and login functionality.

Passwords are handled using the bcrypt cryptographic hashing algorithm. During registration, email uniqueness is checked before the password is hashed and stored.

Incoming requests are validated using Pydantic models.

The `better-profanity` library is also used to detect inappropriate language. When inappropriate content is detected, the processing pipeline is stopped and a system alert is returned.

## Technology Stack

| Component              | Technology                               |
| ---------------------- | ---------------------------------------- |
| Frontend               | HTML5, CSS3, JavaScript                  |
| Frontend Communication | JavaScript Fetch API                     |
| Backend                | Python, FastAPI                          |
| Database               | MySQL                                    |
| LLM                    | Google Gemini                            |
| AI SDK                 | `google.genai`                           |
| RAG                    | Localized Retrieval-Augmented Generation |
| Authentication         | Passlib / bcrypt                         |
| Content Moderation     | better-profanity                         |

## Database

The system uses a MySQL relational database with the following primary entities:

### Users

Stores user authentication and account information.

### Faculty

Stores faculty-related information, including details such as:

* Name
* Department
* Subject
* Cabin
* Teaching skills
* Behaviour
* Internal marking
* Exam marking
* Overall average

### Complaints

Stores administrative complaints along with their status and timestamp.

## User Interface

The frontend is implemented as a responsive Single Page Application.

The report describes the interface as providing:

* User authentication
* Conversational chat
* Typing indicators
* Message timestamps
* Dynamic chat updates
* Navigation between the chat and mess menu
* Responsive web interaction

The frontend uses asynchronous JavaScript to update the interface without requiring browser page reloads.

## Project Objectives

The project was developed with the following objectives:

1. Provide a centralized interface for accessing institution-specific information.
2. Use database-backed context to improve the relevance of LLM responses.
3. Provide secure user authentication using bcrypt.
4. Simplify administrative complaint submission.
5. Store complaints directly in the MySQL database.
6. Provide content moderation for user queries.
7. Develop an interactive and responsive web interface.

## Project Outcomes

The implemented system demonstrated:

* Successful integration of Google Gemini with the MySQL database.
* Localized RAG for retrieving institution-specific information.
* Database-based faculty and mess information retrieval.
* Direct complaint insertion through the `complaint:` command.
* Complaint ID generation and status tracking.
* Bcrypt-based authentication.
* Content moderation using `better-profanity`.
* Asynchronous frontend interaction.

## Team

* Mokshad Tryambak Bunde
* Rohan Sunil Patil
* Pranjal Gupta
* Sai Patil
* Vaibhav Jain
