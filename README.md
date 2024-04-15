# TeamTalk backend
## Stack used :
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height=90/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" height=80/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original.svg"  height=80/><img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original-wordmark.svg"  height=80/>
    
## How to run     
1. Install dependencies
```
pip install --no-cache-dir -r requirements.txt

```

1. Add env variables
```
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DB_NAME
PG_EMAIL
PG_PASSWORD
```

2. Run docker compose
Here we initialize the Postgres image with a pgAdmin GUI
```
docker compose up
```

3. Run uvicorn server
Here we start our uvicorn server in port 8000
```
uvicorn app.main:app --reload
```