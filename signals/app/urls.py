from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index,name='index'),
    path('profile',views.create_user_profile,name='create_user_profile'),
    path('books',views.create_book,name='books'),
    path('delete_profile',views.delete_user,name='delete_user_profile'),
]