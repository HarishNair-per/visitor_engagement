from django.urls import path
from . import views

app_name = 'visitor'



urlpatterns = [
    path('table/', views.visitor_table, name='visitor_table'),
    
    path('register/', views.visitor_form_view, name='visitor_form'),
    path('api/register/', views.visitor_register, name='visitor_api'),

    
    path('update/<str:pk>', views.visitor_update, name='visitor_update'),
]

#path('success/', views.success, name='success'),