from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('featured/', views.FeaturedProjectsView.as_view(), name='featured'),
    path('category/<slug:slug>/', views.ProjectCategoryView.as_view(), name='category'),
    path('technology/<slug:slug>/', views.TechnologyView.as_view(), name='technology'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='detail'),
    path('ajax/search/', views.project_search, name='search'),
]
