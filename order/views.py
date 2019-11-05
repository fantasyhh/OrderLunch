from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderRecord
from .serializers import OrderRecordSerializer
from .buttontime import is_rechargetime,is_ordertime


class UserOrderView(APIView):

    def get(self, request):
        """
        user get their order record (latest 10)
        """
        login_user = request.user
        order_record = OrderRecord.objects.filter(user=login_user).order_by('-id')[:10]
        serializer = OrderRecordSerializer(order_record, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """
        user order lunch
        """
        login_user = request.user
        price = request.data['price']
        number = request.data['number']
        if OrderRecord.objects.filter(user=login_user,is_finished=False).exists():
            return Response({'msg': 'Have unfinished order'}, status=403)
        else:
            r = OrderRecord(number=int(number), price=price, user=login_user)
            r.save()
            return Response({'msg': 'Order successfully , wait result'}, status=200)



class  ButtonView(APIView):
    def get(self, request):
        """
        check if in order_time and recharge_time
        """
        button = request.query_params['button']
        if button == 'order':
            return Response({'msg': 'check the result','order': is_ordertime() }, status=200)
        elif button == 'recharge':
            return Response({'msg': 'check the result', 'recharge': is_rechargetime()}, status=200)
        else:
            return Response({'msg': 'error query parmas'}, status=400)

