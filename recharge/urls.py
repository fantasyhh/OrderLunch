from django.urls import path

from .views import UserRechargeView,ShowMoneyView

# django url
urlpatterns = [
    path('recharge/', UserRechargeView.as_view()),
    path('money/', ShowMoneyView.as_view()),
]

