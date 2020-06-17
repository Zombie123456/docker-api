from django.db import models


class House(models.Model):
    CAN_SELA = 0
    CONTROL = 1
    Sign = 2
    FULL_MONEY = 3

    STATUS_OPTION = ((CAN_SELA, '可售房源'), (CONTROL, '销控房源'),
                     (Sign, '签约房源'), (FULL_MONEY, '全款到账'))

    name = models.CharField(max_length=100, null=True, blank=True)
    info = models.TextField()
    room_num = models.CharField(max_length=20, blank=True, null=True)
    area = models.IntegerField(blank=True)
    is_full_money = models.BooleanField(default=False)
    price = models.CharField(max_length=20, blank=True, null=True)
    phone = models.IntegerField(blank=True)
    memo = models.TextField()
    status = models.IntegerField(default=CAN_SELA, choices=STATUS_OPTION)
