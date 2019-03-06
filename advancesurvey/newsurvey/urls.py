from . import views
from django.urls import path,include

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_org/', views.add_org, name='add_org'),
    path('getorgdata/',views.getorgdata,name='getorgdata'),
    path('admin_register/',views.admin_register,name='admin_register'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('Add_Survey/', views.Add_Survey, name='Add_Survey'),

]