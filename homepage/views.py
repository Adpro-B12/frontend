from django.shortcuts import render

def show_homepage(request):
    context = {
        'username': request.COOKIES.get('username')
    }
    return render(request, "homepage.html", context)
