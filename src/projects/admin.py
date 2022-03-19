from django.contrib import admin
from .models import Project, WorkDay, Invoice, InvoiceDetail

# Register your models here.
admin.site.register(Project)
admin.site.register(WorkDay)
admin.site.register(Invoice)
admin.site.register(InvoiceDetail)
