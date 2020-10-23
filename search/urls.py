from django.urls import path

from . import views


app_name = 'search'
urlpatterns = [ #to do include other paths
    path('', views.index, name='index'),
    path('results/<str:Mid>/', views.detail, name='detail'),
    path('contribute/', views.contribute, name='contribute'),
    path('about/', views.about, name='about'), # ta verjetno tud???
   # path('access/', views.access, name='access'), # ta gre ven! povsod!
    path('instructions/', views.instructions, name='instructions'),
]
# še templates