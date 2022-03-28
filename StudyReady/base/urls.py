from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),

    # create-room
    path('create-room/', views.createRoom, name="create-room"),

    # update-room
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),

    # delete-room
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    # delete-message
    path('delete-message/<str:pk>/', views.deleteMsg, name="delete-message"),

    # update-user
    path('update-user/', views.updateUser, name="update-user"),

    # profile
    path('profile/<str:pk>/', views.userProfile, name="profile"),

    # topic page
    path('topics/', views.topicsPage, name="topics"),

    # activity page 
    path('activity/', views.activityPage, name="activity"),
]
