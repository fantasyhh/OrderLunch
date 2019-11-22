from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


# Create your models here
class OrderRecord(models.Model):
    FINISHED_CHOICES = [
        (-1, '订饭失败'),
        (1, '订饭成功'),
        (0, '等待管理员确认'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="序号")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, verbose_name='用户')
    price = models.IntegerField(verbose_name='价格', default=10)
    number = models.IntegerField(verbose_name='数量', default=1)
    is_finished = models.IntegerField(default=0, verbose_name='订饭状态', choices=FINISHED_CHOICES)
    created = CreationDateTimeField(verbose_name='订餐时间')
    modified = ModificationDateTimeField(verbose_name='最后修改时间')

    class Meta:
        db_table = 'T_Order'
        verbose_name_plural = '订饭记录'

    def __str__(self):
        return "{} order {}  price-{}-lunch".format(self.user.username, self.number, self.price)
