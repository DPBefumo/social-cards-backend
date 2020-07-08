from django.db import models
from users.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Q

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

COLOR_CHOICES = (
    ('Ash Gray', 'Ash Gray'),
    ('Gunmetal', 'Gunmetal'),
    ('Baby Powder', 'Baby Powder'),
    ('Indigo Dye', 'Indigo Dye'),
    ('Ivory', 'Ivory'),
)

BORDER_CHOICES = (
    ('groove', 'groove'),
    ('solid', 'solid'),
    ('dotted', 'dotted'),
    ('ridge', 'ridge'),
    ('none', 'none')
)

FONT_CHOICES = (
    ('Lora', 'Lora'),
    ('Merriweather', 'Merriweather'),
    ('Proza Libre', 'Proza Libre'), 
    ('Open Sans', 'Open Sans'),
    ('Libre Baskerville', 'Libre Baskerville'), 
    ('Source Sans Pro', 'Source Sans Pro'),
    ('BioRhyme', 'BioRhyme'), 
    ('Cabin', 'Cabin'),
)

class Card(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='cards', null=True, editable=False)
    posted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=100, choices=COLOR_CHOICES, default='', null=True)
    border = models.CharField(max_length=100, choices=BORDER_CHOICES, default='', null=True)
    font = models.CharField(max_length=100, choices=FONT_CHOICES, default='', null=True)




