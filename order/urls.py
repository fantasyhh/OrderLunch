from django.urls import path

from .views import UserOrderView,ButtonView

# django url
urlpatterns = [
    path('order/', UserOrderView.as_view()),
    path('button/', ButtonView.as_view()),
]

