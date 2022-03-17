from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User
from jalali_date.widgets import AdminJalaliDateWidget
from .models import Project, WorkDay


class ProjectsForm(forms.ModelForm):
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if end_date < start_date:
            raise ValidationError('تاریخ اتمام نمی تواند کوچک تر از تاریخ شروع باشد')
        return end_date

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'نام پروژه'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'توضیحات',
                    'id': 'kt-ckeditor-1'
                }
            ),
            'department': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'دپارتمان',
                    'id': 'kt-ckeditor-1'
                }
            ),
            'customers': forms.SelectMultiple(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'کارفرمایان'
                }
            ),
            'accessibility': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg form-control-solid', 'placeholder': 'دسترسی ها'
                }
            ),
            'start_date': AdminJalaliDateWidget(
                attrs={
                    'autocomplete': 'off',
                },
            ),
            'end_date': AdminJalaliDateWidget(
                attrs={
                    'autocomplete': 'off',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['customers'].queryset = User.objects.filter(is_customer=True)


class WorkDaysForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = '__all__'
        widgets = {
            'date': AdminJalaliDateWidget(
                attrs={'autocomplete': 'off', }
            ),
            'start_time': forms.TimeInput(
                attrs={'class': 'form-control'}
            ),
            'end_time': forms.TimeInput(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employees'].queryset = User.objects.filter(is_employee=True)
