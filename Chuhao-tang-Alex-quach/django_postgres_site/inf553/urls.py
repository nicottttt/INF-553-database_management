from django.urls import path
from . import views

urlpatterns = [
    path('', views.journal, name='journal'),
    path('journal:<str:journal_name>/', views.journal_detail, name='journal_detail'),
    path('author:<str:author_name>/', views.author, name='author'),
]