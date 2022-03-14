from django.views.generic import ListView
from accounts.models import User


# Create your views here.
class UsersList(ListView):
    def get_queryset(self):
        users = User.objects.all().order_by('-id')
        filter_params = self.request.GET.get('filter')
        if filter_params == 'customer':
            return users.filter(is_customer=True)
        elif filter_params == 'employee':
            return users.filter(is_employee=True)
        elif filter_params == 'manager':
            return users.filter(is_superuser=True)
        elif filter_params == 'supporter':
            return users.filter(is_supporter=True)
        elif filter_params == 'admin':
            return users.filter(is_admin=True)
        return users

    template_name = 'managers/user_list.html'
    context_object_name = 'users'
    paginate_by = 9
