from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('import/', views.import_album, name='import_album')
]