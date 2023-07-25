from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['fname']) <2:
            errors['fname'] = " First Name should be at least 2 characters"
        if not postData['fname'].isalpha():
            errors['fnameformat'] = " First Name should be only alphabatical characters"
        if len(postData['lname']) <2:
            errors['name'] = " Last Name should be at least 2 characters"
        if not postData['lname'].isalpha():
            errors['lnameformat'] = "Name should be only alphabatical characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid Email address"
        if len(postData['password']) <8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors['matchpwd'] = "you have to enter the same password in the confirm password field"
        users = User.objects.filter(email= postData['email'])
        if users:
            errors['userexisting']= "this email is already registered, you can login "
        return errors
    
    def login_validator(self, postData):
        errors={}
        users = User.objects.filter(email= postData['email'])
        if users:
            logged_user=users[0]
            inserted_pwd=postData['password']
            if not bcrypt.checkpw(inserted_pwd.encode(), logged_user.password.encode()):
                errors['log']="password is incorrect"
        else:
            errors['noemail']= "this email is not registered"
        return errors
