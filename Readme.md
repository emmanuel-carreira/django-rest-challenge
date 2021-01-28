# Django REST Challenge

## Setup

### Build image and container
docker-compose up -d --build

### Apply migrations
docker exec -it djangorestchallenge_web_1 bash
python manage.py migrate

### Create superuser
python manage.py createsuperuser