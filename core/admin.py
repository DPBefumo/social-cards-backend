from django.contrib import admin
from .models import Card
from rest_framework.authtoken.admin import TokenAdmin

# Register your models here.
admin.site.register(Card)
TokenAdmin.raw_id_fields = ['user']