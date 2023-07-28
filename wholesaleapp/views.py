from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import User, Representative
from django.http import JsonResponse
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
        request.session['id']=logged_user.id
        return redirect ('/home')

def reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        user = User.objects.create (
            name= request.POST['name'],
            adress= request.POST['adress'],
            telephone_number= request.POST['phone_number'], #the comma after phone number wasn't there I added
            email= request.POST['email'],
            password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
        request.session['id']=user.id
        return redirect ('/home')

def home(request):
    my_user = User.objects.get(id =request.session['id'])
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
    context = {
        'rep':rep
    }
    return render(request,'edit_rep.html',context)

def edit_it(request):
    rep = Representative.objects.get(id = request.POST['rep_id'])
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



def check_details(request):
    if request.method == 'POST':
        rep_id = request.POST.get('rep_id')
        if rep_id:
            rep = get_object_or_404(Representative, id=rep_id)
            return render(request, 'view_rep.html', {'rep': rep})
        else:
            
            return redirect('/home')
    else:
        rep_id = request.GET.get('rep_id')
        if rep_id:
            rep = get_object_or_404(Representative, id=rep_id)
            return render(request, 'view_rep.html', {'rep': rep})
        else:
            return redirect('/home')
        
def comp_view(request,id):
    company = User.objects.get(id = id)
    context = {
        'company':company
    }
    return render(request,'company_view.html',context)

def get_company_names(request):
    search= request.GET.get('term')
    objects=User.objects.filter(name__icontains=search)
    results =[{'id': company.id, 'name': company.name} for company in objects]
    return JsonResponse(results, safe=False)