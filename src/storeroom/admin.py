from django.contrib import admin
from .models import Kala, KalaDetail, KalaHistory

# Register your models here.
admin.site.register(Kala)
admin.site.register(KalaDetail)
admin.site.register(KalaHistory)
