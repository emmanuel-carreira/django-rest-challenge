from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(_('E-mail'), unique=True)
    first_name = models.CharField(_('Nome'), max_length=30)
    last_name = models.CharField(_('Sobrenome'), max_length=30)
    created_at = models.DateTimeField(_('Data de criação'), auto_now_add=True)
    last_login = models.DateTimeField(_('Último login'), auto_now_add=True)
    is_active = models.BooleanField(_('Ativo'), default=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Phone(models.Model):
    number = models.PositiveIntegerField(_('Número'))
    area_code = models.PositiveSmallIntegerField(_('DDD'))
    country_code = models.CharField(_('DDI'), max_length=4)
    profile = models.ForeignKey(
        User, verbose_name=_('Usuário'),
        on_delete=models.CASCADE, related_name='phones'
    )

    def __str__(self):
        return f'{self.country_code} {self.area_code} {self.number}'
