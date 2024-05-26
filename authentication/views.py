from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
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
            response_data = r.json().get("data", {})
            token = response_data.get("token")

            r = requests.get(f"http://34.126.177.181/auth/profiles/{username}", headers=headers)
            profile = r.json() if r.status_code == 200 else None
            role = profile.get('role', None)
            
            if token:
                resp = redirect(reverse("authentication:profile_detail", kwargs={"username": username}))
                resp.set_cookie("Authorization", "Bearer " + token)
                resp.set_cookie("username", username)
                resp.set_cookie("role", role)  # Simpan role pengguna dalam cookie
            else:
                raise ValueError("Token not found in the response")
            return resp
        else:
            messages.error(request, "Incorrect username or password")
    
    return render(request, "login.html", {})

@csrf_exempt
def logout_user(request):
    headers = {'Authorization': request.COOKIES.get('Authorization')}
    r = requests.post("http://34.126.177.181/auth/logout", headers=headers)
    if r.status_code == 200:
        response = HttpResponseRedirect(reverse('homepage:show_homepage'))
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        return response
    else:
        messages.error(request, "Logout failed.")
        return redirect('authentication:profile_detail', username=request.COOKIES.get('username'))

def profile_detail(request, username):
    headers = {'Authorization': request.COOKIES.get('Authorization')}
    r = requests.get(f"http://34.126.177.181/auth/profiles/{username}", headers=headers)
    profile = r.json() if r.status_code == 200 else None
    role = request.COOKIES.get('role')
    if profile is None:
        return HttpResponseNotFound("Profile not found")
    return render(request, "profile_detail.html", {'profile': profile, 'role': role})

@csrf_exempt
def profile_edit(request, username):
    headers = {'Authorization': request.COOKIES.get('Authorization')}
    role = request.COOKIES.get('role')
    if request.method == "POST":
        data = json.dumps({
            "username": request.POST.get("username"),
            "fullName": request.POST.get("fullName"),
            "email": request.POST.get("email"),
            "phoneNumber": request.POST.get("phoneNumber"),
            "address": request.POST.get("address"),
            "role": role
        })
        headers['Content-Type'] = 'application/json'
        r = requests.put(f"http://34.126.177.181/auth/profiles/{username}", data=data, headers=headers)
        if r.status_code == 200:
            messages.success(request, "Profile updated successfully.")
            return redirect('authentication:profile_detail', username=username)
        else:
            messages.error(request, "Failed to update profile.")
    
    r = requests.get(f"http://34.126.177.181/auth/profiles/{username}", headers=headers)
    profile = r.json() if r.status_code == 200 else None
    if profile is None:
        return HttpResponseNotFound("Profile not found")
    return render(request, "profile_edit.html", {'profile': profile, 'role': role})

@csrf_exempt
def profile_delete(request, username):
    headers = {'Authorization': request.COOKIES.get('Authorization')}
    if request.method == "POST":
        r = requests.delete(f"http://34.126.177.181/auth/profiles/{username}", headers=headers)
        if r.status_code == 204:
            messages.success(request, "Profile deleted successfully.")
            response = HttpResponseRedirect('/')
            response.delete_cookie('Authorization')
            response.delete_cookie('username')
            return response
        else:
            messages.error(request, "Failed to delete profile.")
    return render(request, "profile_delete.html", {'username': username})