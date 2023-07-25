from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# render login page
def log(request):
    request.session['logged']= False
    return render (request,'log.html')

# validate login and redirect to home page
def login(request):
    postData=request.POST
    errors = User.objects.login_validator(postData)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        users=User.objects.filter(email=request.POST['email'])
        logged_user=users[0]
        request.session['name']=f"{logged_user.fname} {logged_user.lname}"
        request.session['logged']=True
    return redirect ('/home')

def reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        User.objects.create (
            fname= request.POST['fname'],
            lname= request.POST['lname'],
            email= request.POST['email'],
            password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
    return redirect ('/')

def home(request):
    pass

# log out the site and delete all session data'
def logout(request):
    if request.method == 'POST':
        del request.session['loggedUser']
        request.session['logged']= False
        request.session.flush()
    return redirect ('/')
