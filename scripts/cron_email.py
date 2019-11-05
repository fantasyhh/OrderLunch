import serial
from order.models import OrderRecord
from django.core.mail import send_mail
from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client


def send_notice(arduino=False,email=True):
    order_queryset = OrderRecord.objects.filter(is_finished=False)
    if order_queryset.exists():
        price_12 = order_queryset.filter(price=12).count()
        price_10 = order_queryset.filter(price=10).count()
        total = price_12 * 12 + price_10 * 10
        if arduino:
            ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
            arduino_notice = "order_{:0>2}_{:0>2}".format(price_10,price_12)
            ser.write(arduino_notice.encode('ascii'))
        if email:
            admin_site = '192.168.122.99:8080/admin/'
            send_mail('今日订饭信息',
                      '今日订饭 十二元{}份  十元{}份 总计饭钱{}元 ,请到{}确认'.format(price_12, price_10, total, admin_site),
                      'shijiahuan2610@163.com', ['baird_shi@amaxchina.com'], fail_silently=False)
    else:
        print('Today no lunch ordered, may be in hoilday !')



# """
# 管理员email确认,过25分钟再用短信
def send_messege():
    order_queryset = OrderRecord.objects.filter(is_finished=False)
    if order_queryset.exists():
        account_sid = 'your twilio account sid'
        auth_token = 'your twilio auth token'
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body="都快要十点了，管理员还没确定订饭信息,赶紧的!",
            from_='+12063124257',
            to='+8618952458263')


def run():
    # BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(send_notice, 'cron', day_of_week='0-6', hour=9, minute=30)
    # scheduler.add_job(send_messege, 'cron', day_of_week='0-6', hour=9, minute=50)
    scheduler.start()
