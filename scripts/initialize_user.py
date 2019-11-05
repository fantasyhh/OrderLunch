from django.contrib.auth.models import Permission, User

super_users = {'baird_shi'}
admin_users = {'catherine_lu'}

pse_users = {'baird_shi', 'niki_zuo', 'hanson_li', 'julian_chen', 'miles_xu', 'charles_zhang'}

users = super_users | admin_users | pse_users
admin_permission = Permission.objects.filter(codename__startswith='view')


def run():
    # create user
    for user in users:
        user_email = '{}@amaxchina.com'.format(user)
        # superuser
        if user == 'baird_shi':
             superuser = User.objects.create_superuser(username=user, email=user_email, password=user)
             superuser.save()
        elif user in admin_users:
            admin = User.objects.create_user(username=user, email=user_email, password=user, is_staff=True)
            admin.user_permissions.set(admin_permission)
            admin.save()
        else:
             common_user = User.objects.create_user(username=user, email=user_email, password=user)
             common_user.save()
    print("initialize user successfully ~")