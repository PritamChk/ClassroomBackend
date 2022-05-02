# 4 th Sem Major `Project`

---

## Classroom [LMS]

---

### Contributors

---

> - [Pritam Chakraborty](https://github.com/PritamChk)
> - [Rimi Mondal](https://github.com/RimiDeb13)

> #### Project Start Date : 5-Feb-2022
>
> ###### Coding Start Date : 26-April-2022

---

### Technology Used

---

- [**`python`** (>= 3.10.2)](https://www.python.org/)
- [**`django`** (>= 4.0)](https://docs.djangoproject.com/en/4.0/intro/install/)
- [**`django-rest-framework`** (>= 3.13.1)](https://www.django-rest-framework.org/)
- [`djoser` (>= 2.0)](https://djoser.readthedocs.io/en/latest/getting_started.html)
- [`simple-jwt` (NA)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)
- [`drf-yasg` (NA)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/drf_yasg_integration.html)
- [`django-debug-toolbar` (>= 3.2.4)](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

---

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
