from django.db import models


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Phone(models.Model):
    number = models.PositiveIntegerField()
    area_code = models.PositiveSmallIntegerField()
    country_code = models.CharField(max_length=4)
    phone = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.country_code} {self.area_code} {self.number}'
