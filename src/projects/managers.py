from django.db import models
from django.shortcuts import get_object_or_404


class ProjectManager(models.Manager):
    def get_project_for_staff(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, department__staff_users__in=[user], department__is_active=True
        )
        return qs

    def get_project_for_customer(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, customers__in=[user], department__is_active=True, accessibility='only_customer'
        )
        return qs


class WorkDayManager(models.Manager):
    def filter_workday(self, from_date, to_date, accessibility):
        return self.filter(
            date__gte=from_date,
            date__lte=to_date,
            accessibility=accessibility
        ).all()

    def get_work_day_for_staff(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, project__department__staff_users__in=[user], project__department__is_active=True
        )
        return qs

    def get_work_day_for_customer(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, project__customers__in=[user], project__department__is_active=True,
            project__accessibility='only_customer', accessibility='only_customer'
        )
        return qs


class InvoiceManager(models.Manager):
    def get_invoice_for_staff(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, project__department__staff_users__in=[user], project__department__is_active=True
        )
        return qs

    def get_invoice_for_customer(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, project__customers__in=[user], project__department__is_active=True,
            project__accessibility='only_customer'
        )
        return qs
