from django.shortcuts import render


# Create your views here.
def staff_home_page(request):
    return render(request, 'staff/staff_home_page.html')
