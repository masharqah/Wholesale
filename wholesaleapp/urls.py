from django.urls import path     
from . import views

urlpatterns = [ 
    path('', views.log, name='loginPage'),
    path('login', views.login, name='logged'),
    path('home',views.home , name='mainPage'),
    path('reg', views.reg, name = 'reg'),
    path('logout', views.logout, name='logout'),
    # path('user_view/<int:id>',views.user_view, name = 'companyView'), #redirect to the company view page (that has company details)
    path('add_rep',views.add_rep),
    path('add',views.adding),
    path('edit/<int:id>',views.edit),
    path('edit_it',views.edit_it),
    path('delete/<int:id>',views.delete),
    # path('view/<int:id>',views.view_rep), #this displays the representative's details
    path('check_details/', views.check_details, name='check_details'),
    # path('createcompany', views.createcompany),
    path('edit/<int:rep_id>/', views.edit, name='edit_rep'),
    path('delete/<int:rep_id>/', views.delete, name='delete_rep'),
    path('comp_view/<int:id>',views.comp_view, name='company_view'),
    path('autocomplete/', views.get_company_names, name = 'company-autocomplete'),
]