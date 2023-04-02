# B2B Shop
A B2B e-shop for selling cellular charge for businesses written with Django and DRF(Django Rest Framework)

## Installation and Setup
Clone this repository to your local machine:
```
git clone https://github.com/ialphaw/b2b_shop.git
```
Install Docker on your machine. Refer to the Docker documentation for installation instructions for your platform.

Open a terminal in the root directory of the cloned repository then follow this steps:

1- create .env file from .env.sample and fill this:
```
cp core/.env.sample core/.env
```
* for fill the 'SECRET_KEY' you can using the terminal by running the following command:
```
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
or use online Django 'SECRET_KEY' genarators like: https://djecrety.ir

2- build the Docker image:
```
docker-compose up --build
```
Access the B2B Shop app in your web browser at: http://127.0.0.1:8001/swagger/.
