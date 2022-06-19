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

[![Click on it](./readme/BackendAPI_Doc.jpeg)](readme\whole_sw_review.mp4)
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

# Recommended Setup

---

> **Install** :

1. [VS Code](https://code.visualstudio.com/)
   2.Install [Docker](https://www.docker.com/get-started/) & Run It
2. Save `docker-entrypoint.sh` & `wait-for-it.sh` with `LF` line feed.
3. use the following command for first time build:

```powershell
docker-compose up --build
```

5. create super user for django admin area
   (one time)

```bash
docker-compose run web python manage.py createsuperuser
```

6. for other commands check out the `Pipfile`

---

## Some Glimpse of Frontend :

---

<p float="left">
<img src="./readme/HomePage.jpeg">
</p>

<p float="left">
<img src="./readme/SignUpPage.jpeg" style="width: 49%;height: 50%">
<img src="./readme/LogInPage.jpeg" style="width: 49%;height: 50%">
</p>

<p float="left">
<img src="./readme/CreateCollegePage.jpeg" style="width: 49%;height: 50%">
<img src="./readme/SubjectAddByStudent.jpeg" style="width: 49%;height: 50%">
</p>
---

## To Know More About Frontend :
> #### [Click Here [↗]](https://github.com/TathagataDas99/Classroom-Frontend)

---
