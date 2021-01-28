from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    first_name = models.CharField(_('Nome'), max_length=50)
    last_name = models.CharField(_('Sobrenome'), max_length=50)
    email = models.EmailField(_('E-mail'), unique=True)
    password = models.CharField(_('Senha'), max_length=255)
    created_at = models.DateTimeField(_('Data de criação'), auto_now_add=True)
    last_login = models.DateTimeField(_('Último login'), auto_now_add=True)

    class Meta:
        ordering = ['email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Phone(models.Model):
    number = models.PositiveIntegerField(_('Número'))
    area_code = models.PositiveSmallIntegerField(_('DDD'))
    country_code = models.CharField(_('DDI'), max_length=4)
    profile = models.ForeignKey(
        Profile, verbose_name=_('Perfil'),
        on_delete=models.CASCADE, related_name='phones'
    )

    def __str__(self):
        return f'{self.country_code} {self.area_code} {self.number}'
