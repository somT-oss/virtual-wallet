# virtual-wallet

Crenet Backend Developer task, building a virtual wallet.

### Tooling
- django rest framework
- SQlite3 database 
- Postman (API Testing)
- django rest framework simplejwt (Token Authentication)

### Overview
This is the backend API task from CRENET completed using the following tools listed above. 
I completed all the challenges and implemented all the features needed for this API.

### Setup

- Clone github repository
    - ```git clone https://github.com/somT-oss/virtual-wallet.git```
- Create virtual environment
    - ```virtualenv env```
    - ``` source env/bin/activate```
- Install requirements
    - ``` pip install -r requirements.txt ```
- Run development server
    - ``` python manage.py runserver```
- Create admin user 
    - ```python manage.py createsuperuser```
- Login to admin dashboard 
    - ```localhost:8000/admin```
 
### Endpoints (with token authorization)

- Register users ```localhost:8000/users/register```
- Login users  ```localhost:8000/users/login```
- Update users ```localhost:8000/users/update/{firstname}```
- Get all wallets ```localhost:8000/wallet/all-wallet```
- Get one user wallet ```localhost:8000/wallet/get-user-wallet/{user-id}```
- Fund all user wallets ```localhost:8000/wallet/fund-all-wallet```
- Fund one user wallet ```localhost:8000/wallet/fund-user-wallet/{user-id}```
