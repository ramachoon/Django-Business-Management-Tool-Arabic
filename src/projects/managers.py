from django.db import models
from django.utils import timezone


class WorkDayManager(models.Manager):
    def filter_workday(self, from_date, to_date, accessibility):
        return self.filter(
            date__gte=from_date,
            date__lte=to_date,
            accessibility=accessibility
        ).all()
