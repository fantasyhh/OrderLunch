from django.contrib import admin, messages
from django.db.models import F, Sum

from .models import RechargeRecord, Money

admin.site.index_title = 'AMAX订饭系统'
admin.site.site_header = '站点管理'
admin.site.site_title = '站点管理'


@admin.register(RechargeRecord)
class RechargeRecordAdmin(admin.ModelAdmin):
    # 管理员操作
    actions = ['ensure_recharge','refuse_recharge','sum_recharge']

    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'user', 'amount', 'created', 'is_finished')

    list_filter = ('is_finished',)

    # action1
    def ensure_recharge(self, request, queryset):
        for obj in queryset:
            if not obj.is_finished:
                # change money
                m = obj.user.money
                m.balance = F('balance') + obj.amount
                m.save()
                # change is_finished
                obj.is_finished = True
                obj.save()

    ensure_recharge.short_description = "确认充值金额准确，完成充值操作"

    #action2
    def refuse_recharge(self,request, queryset):
        queryset.filter(is_finished=0).update(is_finished=-1)

    refuse_recharge.short_description = "由于数值数额不一致或者备注用户名等原因,拒绝充值该金额"

    # 　action3
    def sum_recharge(self, request, queryset):
        total = queryset.aggregate(Sum('amount'))
        messages.success(request, "你所勾选充值记录的总金额为{}元～".format(total['amount__sum']))

    sum_recharge.short_description = "查看所勾选的充值总额"


@admin.register(Money)
class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')

    # list_display_links = ('id', 'user')
    list_display_links = None

    readonly_fields = list_display

    # def has_add_permission(self, request):
    #     if not request.user.is_superuser:
    #         return False
    #
    # def has_change_permission(self, request, obj=None):
    #     if not request.user.is_superuser:
    #         return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     if not request.user.is_superuser:
    #         return False
