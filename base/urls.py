from django.urls import path

from . import views

urlpatterns = [
    path('login',views.loginPage,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('register',views.registerUser,name="register"),

    path('',views.home,name="home"),
    path('room/<int:pk>/',views.room,name="room"),
    path('profile/<int:pk>/',views.userProfile,name="user-profile"),
    path('topics/',views.topicsPage,name="topics"),
    path('activity/',views.activityPage,name="activity"),
    
    path('create-room',views.createRoom, name="create-room"),
    path('update-room/<int:pk>/',views.updateRoom, name="update-room"),
    path('delete-room/<int:pk>/',views.deleteRoom, name="delete-room"),
    path('delete-message/<int:pk>/',views.deleteMessage, name="delete-message"),
    
    path('update-user/',views.updateUser, name="update-user"),
    
    #follow-topic
    path('follow_topic/<int:topic_id>',views.followTopic,name="follow-topic"),

    #follow-user
    path('follow_user/<int:user_id>',views.followUser,name="follow-user")
]