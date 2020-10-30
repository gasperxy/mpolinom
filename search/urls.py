from django.urls import path

from . import views


app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/<str:Mid>/', views.detail, name='detail'),
    path('contribute/', views.contribute, name='contribute'),
    path('instructions/', views.instructions, name='instructions'),
]




#  path('about/', views.about, name='about'), # ta verjetno ven?
#acc

# še templates
