# Django REST Challenge

## Setup

### Build image and container
docker-compose up -d --build

### Apply migrations
docker exec -it web bash
./startup.sh

### Create superuser
python manage.py createsuperuser