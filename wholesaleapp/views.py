from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Representative
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
        request.session['name']=f"{logged_user.name}"
        request.session['logged']=True
        request.session['id']=users.id
    return redirect ('/home')

def reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        User.objects.create (
            name= request.POST['name'],
            adress= request.POST['name'],
            phone_number= request.POST['phone_number'], #the comma after phone number wasn't there I added
            email= request.POST['email'],
            password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
    return redirect ('/')

def home(request):
    my_user = User.objects.get(id =request.session['id'] )
    users = User.objects.all()
    reps = Representative.objects.all()
    context = {
        'my_user' : my_user,
        'users' : users,
        'reps' : reps,
    }
    return render(request,'stores_display.html',context)


# log out the site and delete all session data'
def logout(request):
    if request.method == 'POST':
        del request.session['loggedUser']
        request.session['logged']= False
        request.session.flush()
    return redirect ('/')

def add_rep(request):
    return render(request,'add_rep.html')

def adding(request):
    company = User.objects.get(id = request.session['id'])
    name = request.POST['rep_name']
    phone_no = request.POST['phone_no']
    email = request.POST['email']
    city= request.POST['city']
    Rep = Representative.objects.create(name = name,phone_no = phone_no,email = email, city=city ,company = company )
    Rep.save()
    return redirect('/home')

def edit(request,id):
    rep = Representative.objects.get(id =id)
    return render(request,'add_rep.html',rep)

def edit_it(request):
    rep = User.objects.get(id = request.POST['rep_id'])
    rep.name = request.POST['rep_name']
    rep.phone_no = request.POST['phone_no']
    rep.email = request.POST['email']
    rep.city= request.POST['city']
    rep.save()
    return redirect('/home')

def delete(request,id):
    rep_delete = Representative.objects.get(id = id)
    rep_delete.delete()
    return redirect('/home')