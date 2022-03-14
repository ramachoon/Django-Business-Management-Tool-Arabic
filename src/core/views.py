from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='account:login')
def main_view(request):
    return HttpResponse('خوش آمدید')
