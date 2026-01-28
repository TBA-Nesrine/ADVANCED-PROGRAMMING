from django.shortcuts import render

def home(request):
    return render(request, 'library_app/templates/user_home.html')  # or user_home.html