from django import forms

from accounts.models import User
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description', 'staff_users', 'is_active', 'maker')
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': '5'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff_users'].queryset = User.objects.filter(is_staff=True)
        self.fields['maker'].required = False
