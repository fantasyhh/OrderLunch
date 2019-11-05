from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RechargeRecord
from .serializers import RechargeRecordSerializer


class UserRechargeView(APIView):

    def get(self, request):
        """
        user get their recharge record
        """
        login_user = request.user
        recharge_record = RechargeRecord.objects.filter(user=login_user).order_by('-id')[:10]
        serializer = RechargeRecordSerializer(recharge_record, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        recharge for user
        """
        login_user = request.user
        amount = request.data['amount']
        # if RechargeRecord.objects.filter(user=login_user,is_finished=False).exists():
        #     return Response({'msg': 'Have unfinished recharge'}, status=403)
        # else:
        r = RechargeRecord(amount=int(amount), user=login_user)
        r.save()
        return Response({'msg': 'Recharge successfully , wait result'}, status=200)


class ShowMoneyView(APIView):
    def get(self, request):
        login_user = request.user
        balance = login_user.money.balance
        return Response({'money': balance}, status=200)