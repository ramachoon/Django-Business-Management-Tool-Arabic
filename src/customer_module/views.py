from django.shortcuts import render
from core.decorators import customer_access_decorator


# Create your views here.


@customer_access_decorator()
def customer_home_page(request):
    context = {
        'text': 'داشبورد کارفرما'
    }
    return render(request, 'core/panel/pages/panel_home_page.html', context)
