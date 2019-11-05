import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                print("now login : {}, role: {}".format(user, 'admin'))
            elif user.is_staff:
                print("now login : {}, role: {}".format(user, 'access admon'))
            else:
                print("now login : {}, role: {}".format(user, 'common user'))
            return Response({'msg': 'Log in successfully','user':username}, status=200)
        else:
            # Return an 'invalid login' error message.
            return Response({'msg': 'Unmatched password or username'}, status=401)


class ChangePassword(APIView):

    def patch(self, request):
        """
        update user password
        """
        data = request.data
        password = data['password']
        old_password = data['old_password']
        login_user  = request.user
        if authenticate(username=login_user.username, password=old_password):
            print("now login : {}".format(login_user))
            login_user.set_password(raw_password=password)
            login_user.save()
            return Response({'msg': 'Change password successfully'}, status=200)
        else:
            return Response({'msg': 'Old password is not correct, please enter again'}, status=401)

class ShowUsers(APIView):

    def get(self, request):
        """
        Return a list of all users.
        """
        login_user = request.user
        if login_user.is_superuser:
            users = User.objects.values('username', 'email')
            users_data = [
                {'username': user['username'], 'email': user['email']} for user in users]
            return Response(users_data, status=200)


class LogOutView(APIView):

    def get(self, request):
        print("before logout : {}".format(request.user))
        logout(request)
        print("after logout : {}".format(request.user))
        return Response({'msg': 'Logout successfully'}, status=200)


from django.http import HttpResponse


def test(request):
    login_user = request.user
    print(login_user)
    # balance = login_user.money.balance
    # return Response({'money': 200}, status=200)
    return HttpResponse({'you are': login_user.username})