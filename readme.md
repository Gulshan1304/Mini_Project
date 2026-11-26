Student Management System

A Flask web app for recording student information and marks for two mid-semester tests.

## Features

- Save a student's name, enrollment number, branch, semester, year, and degree.
- Record MST 1 marks out of 20, then MST 2 marks out of 30 later.
- Display pass or fail for each subject. MST 1 pass mark is 9; MST 2 pass mark is 15.
- Save records locally in `students.json`, or use PostgreSQL when `DATABASE_URL` is set.
- View and delete student records.

## Project files

```text
outputs/
├── app.py
├── requirements.txt
├── students.json          # Local records; excluded from Git
├── public/
│   └── style.css
└── templates/
    └── index.html
```

## Run locally on Windows

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000> in a browser. The local app uses `students.json` unless a PostgreSQL connection URL is configured.
