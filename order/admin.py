from django.contrib import admin, messages
from django.db.models import F, Sum

from .models import OrderRecord


@admin.register(OrderRecord)
class OrderRecordAdmin(admin.ModelAdmin):
    actions = ['ensure_order', 'refuse_order', 'sum_order']

    list_display = ('id', 'user', 'price', 'number', 'created', 'is_finished')

    list_display_links = None

    list_filter = ('is_finished',)

    # action1
    def ensure_order(self, request, queryset):
        for obj in queryset:
            if not obj.is_finished:
                # change money
                m = obj.user.money
                m.balance = F('balance') - (obj.price * obj.number)
                m.save()
                # change is_finished
                obj.is_finished = True
                obj.save()

    ensure_order.short_description = "确认午饭订单"

    # action2
    def refuse_order(self, request, queryset):
        queryset.filter(is_finished=0).update(is_finished=-1)

    refuse_order.short_description = "由于某些原因,拒绝确认该订单"

    # action3
    def sum_order(self, request, queryset):
        total = queryset.aggregate(total=Sum(F('price') * F('number')))
        messages.success(request, "你所勾选订饭交易的总金额为{}元～".format(total['total']))

    sum_order.short_description = "查看所勾选的订饭交易的总额"
