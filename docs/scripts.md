### CMD to Run Server for Frontend

---

```bash
ngrok http 8000
```

### FAKE SMTP MAIL

---

```docker
docker run --rm -it -p 5000:80 -p 2525:25 rnwood/smtp4dev
```

## Celery - Redis CMDs

- pipenv run redis
- celery -A core worker -l info -P eventlet
- or pipenv run celery

## HEROKU CMDS

---

```bash
heroku create app-name
```

output:

```bash
https://app-url.com/ | https://git.heroku.com/app.git
```

> **`lms-classroom-api.herokuapp.com`** add this in allowed_host of prod.py

> **`https://git.heroku.com/lms-classroom-api.git`** heroku git repo

#### config environment variables in heroku

---

```bash
heroku config:set VARIABLE_NAME='value'
```

> ### deploy app

---

- #### step 1: `git remote -vv`
- #### step 2: `git branch`
- #### step 3: push branch to heroku `git push heroku main`

# Docker Build & Start

```bash
docker-compose up --build
```

```docker
docker-compose run web python manage.py createsuperuser
```

---

```bash
docker-compose up
```
