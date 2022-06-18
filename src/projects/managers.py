from django.db import models
from django.shortcuts import get_object_or_404


class WorkDayManager(models.Manager):
    def filter_workday(self, from_date, to_date, accessibility):
        return self.filter(
            date__gte=from_date,
            date__lte=to_date,
            accessibility=accessibility
        ).all()


class ProjectManager(models.Manager):
    def get_project_for_staff(self, pk, user):
        qs = get_object_or_404(
            self, pk=pk, department__staff_users__in=[user], department__is_active=True
        )
        return qs
