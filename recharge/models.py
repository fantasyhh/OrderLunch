from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


# Create your models here
class RechargeRecord(models.Model):
    FINISHED_CHOICES = [
        (-1, '充值失败'),
        (1, '充值成功'),
        (0, '等待管理员确认'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="序号")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, verbose_name='用户')
    amount = models.IntegerField(verbose_name='充值金额')
    is_finished = models.IntegerField(default=0, verbose_name='充值状态', choices=FINISHED_CHOICES)
    created = CreationDateTimeField(verbose_name='充值时间')
    modified = ModificationDateTimeField(verbose_name='最后修改时间')

    class Meta:
        db_table = 'T_Recharge'
        # 末尾不加s
        verbose_name_plural = '充值记录'
        # 末尾加s
        # verbose_name='标签'

    def __str__(self):
        return str(self.user.username) + ", recharge: " + str(self.amount)


class Money(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="序号")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    balance = models.IntegerField(default=0, verbose_name='账户余额')

    class Meta:
        db_table = 'T_Money'
        verbose_name_plural = '账户余额'

    def __str__(self):
        return str(self.user.username) + ", Money : " + str(self.balance)

    @receiver(post_save, sender=User)
    def create_user_money(sender, instance, created, **kwargs):
        if created:
            Money.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_money(sender, instance, **kwargs):
        instance.money.save()
