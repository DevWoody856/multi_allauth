This is the repository for <a href="https://rx-36.life/post/create-an-application-with-multiple-login-pages-with-allauth/" target="_blank">this blog post</a>.  
I made a simple app to have multiple google login form with Allauth.

<img src="https://res.cloudinary.com/dfqctp7bq/image/upload/v1654454030/ezgif.com-gif-maker_1_jvfloe.gif">

## How to download this repo locally and running the application

This description assumes the use of docker and windows11.  
And I use pycharm for my IDE.


1. Enter following command from the command line.
```
git clone https://github.com/DevWoody856/multi_allauth
```

2. After downloading the repo, create an `.env` file in the root of the project.

3. In the .env file you created, write the following.

```python
DEBUG_VALUE=TRUE
SECRET_KEY=*****************************************************


DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db_twologin_8_220530
DB_PORT=5432

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```
Regarding the `SECRET_KEY`, I recommend that you create a dummy key at a place like <a href="https://miniwebtool.com/django-secret-key-generator/" target="_blank">this site</a> and put it in the `.env` file.


As a reminder, `DB_HOST` is the service name of the database in `docker-compose.yaml`.  
In this docker configuration, DB_HOST is `db_twologin_8_220530`.

4. From the **project root**, enter the following command.

```python
docker-compose up --build
```

5. If you success `docker-compose up -build`,   
you can see the message "starting development server at http://0.0.0.0:8022/".   
Once it is up and running, please **open another terminal** while docker running, enter the following command.
   (Be sure to go to the root directory of the project before entering this command)
This is the command that enters the dokcer side and launches the command line.

```python
docker-compose exec backend sh
```

6. When you are ready to enter a command, type the following command.
```python
python manage.py makemigrations
```

7. Then, after that
```python
python manage.py migrate
```

8. Database set is finished.
Enter the following command and the application should start.
```python
python manage.py runserver
```

9. If  you get the following message, it is working.
```python
Starting development server at http://127.0.0.1:8000/
```

### Please note that the actual application is accessed at `http://127.0.0.1:8022/`. 

10. Also, in order for this app to work, you must Oauth2.0 credential from GCP (Google cloud platform) and must be entered into django-admin.  
Please refer to <a href="https://rx-36.life/post/create-two-google-sign-in-for-each-user-type-using-allauth/#chapter8" target="_blank">chapters 8 and 9 of this article</a>.