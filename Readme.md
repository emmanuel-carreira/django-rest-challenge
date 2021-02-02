# Django REST Challenge


Available at [Heroku](
https://django-rest-challenge.herokuapp.com/)

[Swagger file](https://drive.google.com/file/d/1mz6cK7-k3WLItAk3GmGzd7xDsEm-_6Ms/view?usp=sharing)

## Setup

### Build image and container
docker-compose up -d --build

### Apply migrations
docker exec -it web bash
./startup.sh

### Create superuser
python manage.py createsuperuser