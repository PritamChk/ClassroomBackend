# Classroom LMS API (Backend)

---

> #### 4 th Sem Major `Project`
>
> - In this Project I have developed this whole API
> - This API has 5 Modules :
>   - Authentication
>   - Owner Admin
>   - Admin with less privileges
>   - Teacher
>   - Student

---

> **API Doc**
>
> <img src="./readme/BackendAPI_Doc.jpeg" width="100%" height="100%" style="border-radius:10px;float: right;box-shadow:2px 3px rgba(0,0,0,.2);">

---

### Contributors

---

> - [Pritam Chakraborty (Backend Dev & Frontend Designer)](https://github.com/PritamChk)
> - [Tathagata Das (Frontend Developer)](https://github.com/TathagataDas99/)
> - [Rimi Mondal (Tester)](https://github.com/RimiDeb13)

---

> #### Project Start Date : 5-Feb-2022
>
> ###### Coding Start Date : 26-April-2022

---

## Technology Stack

---

<p float="left">
<a href="https://www.python.org/">
<img src="./readme/python.png" width="40" style="margin: 4px"/>
</a>
<a href="https://www.djangoproject.com/start/">
<img src="./readme/djangoIcon.png" width="40" style="margin: 4px 5px"/>
</a>

<a href="https://www.django-rest-framework.org/">
<img src="./readme/drf.png" width="100" style="margin: 4px 5px"/>
</a>

<a href="https://www.fullstackpython.com/celery.html">
<img src="./readme/celery.png" width="80" style="margin: 4px 5px"/>
</a>

<a href="https://redis.io/">
<img src="./readme/redis_icon.png" width="60" style="margin: 4px 5px"/>
</a>

<a href="https://www.docker.com/">
<img src="./readme/Docker.png" width="60" style="margin: 4px 5px"/>
</a>

<a href="https://github.com/rnwood/smtp4dev">
<img src="./readme/smtp.png" width="100" style="margin: 4px 3px"/>
</a>
</p>

> `OS` - `Windows 10`

---

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
