# Alumni Influencer API

A FastAPI backend for alumni registration, profile management, blind bidding, featured alumnus selection, and scheduled automation.

## Features
- Alumni registration and login
- JWT authentication
- Protected profile management
- Blind bidding system
- Daily featured alumnus selection
- Monthly win-limit enforcement
- Scheduled winner automation
- Swagger API documentation

## Tech Stack
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- Passlib/Bcrypt
- APScheduler

## Setup
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Create a `.env` file from `.env.example`
5. Run the server:
   uvicorn app.main:app --reload

## Documentation
- Swagger UI: `/docs`