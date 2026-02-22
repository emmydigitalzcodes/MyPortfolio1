from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('resume/', views.ResumeView.as_view(), name='resume'),
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
]
