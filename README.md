# Basecamp server
A simple api for getting and uploading data gathered from sensors.

## Usage:
Install python dependencies:
```
pip install -r requirements.txt
```

Add database url to `.env` (example url):
```
DATABASE_URL = postgres+asyncpg://user:password@hostname:port/database-name
```

Run development server:
```
uvicorn app.main:app --reload
```
