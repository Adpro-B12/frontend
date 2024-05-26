from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

# Register View
@csrf_exempt
def register(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        fullName = request.POST.get("fullName")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone_num = request.POST.get("phoneNumber")
        address = request.POST.get("address")  # Assuming you have an address field
        role = request.POST.get("role")

        # Ensure the data is sent as JSON
        data = json.dumps({
            "username": username,
            "fullName": fullName,
            "password": password,
            "email": email,
            "phoneNumber": phone_num,
            "address": address,
            "role": role
        })

        # Set headers for JSON
        headers = {'Content-Type': 'application/json'}

        # Post the data
        r = requests.post("http://34.126.177.181/auth/register", data=data, headers=headers)
        if r.status_code == 200:
            print('success reg')
            return redirect("authentication:login")  # make sure to use the correct namespace and URL name
        else:
            print('failed reg')
            messages.error(request, 'Registration failed. Please try again.')
    
    return render(request, "register.html", context)

# Login View
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Changed to username to align with typical Spring Boot auth
        password = request.POST.get("password")
        
        # Data and headers
        data = json.dumps({"username": username, "password": password})
        headers = {'Content-Type': 'application/json'}

        print('data:', data)
        r = requests.post("http://34.126.177.181/auth/login", data=data, headers=headers)
        
        if r.status_code == 200:
            print('success login')
            resp = redirect("subscription_management:box_list")  # Adjust as per your URL names
            # Set the Authorization token as a cookie, retrieved from JSON response
            token = r.json().get("data", {}).get("token")
            if token:
                resp.set_cookie("Authorization", "Bearer " + token)
                resp.set_cookie("username", username)
            else:
                # Handle the case where the token is not found in the response
                raise ValueError("Token not found in the response")
            
            return resp
        else:
            print('failed login')
            messages.error(request, "Incorrect username or password")
    
    return render(request, "login.html", {})

@csrf_exempt
def logout_user(request):
    # logout(request)
    response = HttpResponseRedirect(reverse('homepage:show_homepage'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response