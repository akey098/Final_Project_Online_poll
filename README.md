# Online Poll Project

Web-based polling application built with Flask and SQLite, featuring a modular codebase and a sleek light/dark theme toggle.

## Features

- Create polls with any number of options
- Single-choice or multiple-choice polls
- Vote on polls
- View results as percentage bars with a firework animation
- Delete polls
- Sidebar with total polls & total votes
- Light/dark theme toggle

## Setup & Run

1. **Clone the repo**  
   ```bash
   git clone <your-repo-url>
   cd project
2. **(Optional) Create & activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate    # Windows: venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
   
4. **Start the application**
    ```bash
    python run.py

5. **Visit in your browser**
    http://127.0.0.1:5000

## Resetting the Database
To wipe all polls and start fresh, delete the polls.db file and restart the app:
```bash
rm polls.db
python run.py
