from django.contrib import admin
from .models import CustomUser, Opportunity

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Opportunity)