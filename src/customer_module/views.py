from django.shortcuts import render


# Create your views here.
def customer_home_page(request):
    context = {
        'text': 'داشبورد کارفرما'
    }
    return render(request, 'core/panel/pages/panel_home_page.html', context)
