from django.urls import path     
from . import views

urlpatterns = [ 
    path('', views.log, name='loginPage'),
    path('login', views.login, name='logged'),
    path('home',views.home , name='mainPage'),
    path('reg', views.reg, name = 'reg'),
    path('logout', views.logout, name='logout'),
    path('user_view/<int:id>',views.user_view, name = 'companyView'), #redirect to the company view page (that has company details)
    path('add_rep',views.add_rep),
    path('add',views.adding),
    path('edit/<int:id>',views.edit),
    path('edit_it',views.edit_it),
    path('delete/<int:id>',views.delete),
]