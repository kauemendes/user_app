# USER APP REST APPLICATION
##  Using Flask and Docker

### Install application locally:

To run this project locally make sure to have installed python 3+ on your machine. This is project is not compatible with python 3 lower.
This tutorial in how to install may help you: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos

Clone this repository and follow this steps:

1. Create a virtualenv to run locally:
$ `virtualenv venv`

2. Activate your virtualenv:
$ `source venv/bin/activate`

3. Install requirements for this project:
$ `pip3 install -r requirements.txt`

4. Running migration for your database:
$ `python3 manage.py db init`
$ `python3 manage.py db migrate`
$ `python3 manage.py db upgrade`

5. Run COVERAGE tests at the application:
$ `python3 manage.py cov`
A folder ./tmp will be created with coverage reports on index.html

6. Start you application server:
$ `python3 manage.py runserver`


### Run application on DOCKER:

To run your application on containers make sure to have docker and docker-compose installed. `docker --version` and `docker-compose --version`, may help you.
If you need to install follow this tuotiral: https://docs.docker.com/install/ and https://docs.docker.com/compose/install/

Clone this reposistory and follow this steps:

1. Config your host file of your machine to translate 127.0.0.1 to api.ingresse.local, example on linux or macos:
$ `sudo echo "127.0.0.1   api.ingresse.local " >> /etc/hosts`

2. Compose your docker, you may have to choose between environments dev or prod, by choosing dev.yml or prod.yml:
$ `docker-compose -f docker-compose.yml -f prod.yml up --build` you can add `-d` to run in background

3. After building all environments you can access on your browse http://api.ingresse.local/

4. To create a new user on your new api use the following command:
$ `curl -H "Content-Type: application/json" -X POST -d '{"username": "john", "password": "JohnDoe@01", "password_confirm": "JohnDoe@01"}' http://api.ingresse.local/v1/user`
Basically you have to send a post request to /v1/user

[POST] /v1/user - Creates a new user with {"username": string, "email": *string, "password": string, "password_confirm": string} - *for optional
This will return a URL to confirm the registration just for example. You must enter the URL and confirm de register.

Using basic authentication on header {"Authorization":"Basic TOKEN"}

[GET] /v1/user - Retrieve all logged user information
[PUT] /v1/user - Update logged user information
[DELETE] /v1/user - Delete logged user

5. For authenticate on /v1/api/token
$ `curl -u john:JohnDoe@01 -i -X GET http://api.ingresse.local/v1/api/token`

Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 135
    Access-Control-Allow-Origin: *
    Server: Werkzeug/0.11.11 Python/3.5.2
    Date: Fri, 02 Mar 2018 21:29:18 GMT

    {"token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUyMDAyNzM1OCwiaWF0IjoxNTIwMDI2MTU4fQ.eyJpZCI6MX0.85X0ilvlKxYJwzwAJ-oZfYjhBU4AxSA0o7LJ_Me-4s4"}

6. Get information on /v1/user
$ `curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTUyMDAyNzM1OCwiaWF0IjoxNTIwMDI2MTU4fQ.eyJpZCI6MX0.85X0ilvlKxYJwzwAJ-oZfYjhBU4AxSA0o7LJ_Me-4s4:unused -i -X GET http://api.ingresse.local/v1/user`

Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 130
    Access-Control-Allow-Origin: *
    Server: Werkzeug/0.11.11 Python/3.5.2
    Date: Fri, 02 Mar 2018 21:34:48 GMT

    {
        "email": null,
        "last_name": null,
        "name": null,
        "preferences": null,
        "user_id": 1,
        "username": "john"
    }
