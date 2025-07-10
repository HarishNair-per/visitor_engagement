from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    
 path('', views.home, name='home'),
 path('table/', views.planner_table, name='planner_table'),
 path('register/', views.planner_entry, name='planner_entry'),
 path('update/<str:pk>', views.planner_update, name='planner_update'),   
    ]