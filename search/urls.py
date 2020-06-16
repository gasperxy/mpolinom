from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [ #to do include other paths
    path('', views.index, name='index'),
    path('results/<int:polynomial>/', views.detail, name='detail'),
]