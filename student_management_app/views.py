# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app import models


def home(request):
    return render(request, 'landing.html')


def loginPage(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == '1':
            return redirect('admin_home')
        elif user_type == '2':
            return redirect('staff_home')
        elif user_type == '3':
            return redirect('student_home')
    return render(request, 'login.html', {'user_type': 'admin'})


def unified_login(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == '1':
            return redirect('admin_home')
        elif user_type == '2':
            return redirect('staff_home')
        elif user_type == '3':
            return redirect('student_home')
    return render(request, 'unified_login.html')


def student_login(request):
    if request.user.is_authenticated and request.user.user_type == '3':
        return redirect('student_home')
    return render(request, 'student_login.html', {'user_type': 'student'})


def staff_login(request):
    if request.user.is_authenticated and request.user.user_type == '2':
        return redirect('staff_home')
    return render(request, 'staff_login.html', {'user_type': 'staff'})


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = EmailBackEnd.authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            
            # Get the user type and redirect accordingly
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='login')
def student_notifications(request):
    student = models.Students.objects.get(admin=request.user.id)
    notifications = models.NotificationStudent.objects.filter(student_id=student).order_by('-created_at')
    return render(request, 'student_template/student_notifications.html', {'notifications': notifications})


