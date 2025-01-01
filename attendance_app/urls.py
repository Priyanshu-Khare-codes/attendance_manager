from django.urls import path
from. import views

urlpatterns = [
    path('', views.attendance_calculater, name='attendance_calculater'),
    path('result/', views.attendance_result, name='attendance_result'),
    path('about/', views.about, name='about'),
    path('developers/', views.developers, name='developers'),
]  