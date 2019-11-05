from django.urls import path

from .views import LoginView, ChangePassword, ShowUsers, LogOutView,test

# django url
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('changepassword/', ChangePassword.as_view()),
    path('showusers/', ShowUsers.as_view()),
    path('test/',test),
]

