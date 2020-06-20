from django.db import models
from account.models import Staff


class BuildNum(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class House(models.Model):
    CAN_SELA = 0
    CONTROL = 1
    Sign = 2
    FULL_MONEY = 3

    STATUS_OPTION = ((CAN_SELA, '可售房源'), (CONTROL, '销控房源'),
                     (Sign, '签约房源'), (FULL_MONEY, '全款到账'))

    floor = models.IntegerField(null=True, blank=True)
    room_num = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    area = models.FloatField(blank=True, default=0.0)
    unit_type = models.CharField(max_length=20, null=True, blank=True)
    unit_price = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    is_full_money = models.BooleanField(default=False)
    phone = models.CharField(blank=True, null=True, max_length=20)
    memo = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=CAN_SELA, choices=STATUS_OPTION)
    sela_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    build_num = models.ForeignKey(BuildNum, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.room_num}-{self.area}'


class CarSet(models.Model):

    CAN_SELA = 0
    CONTROL = 1
    Sign = 2
    FULL_MONEY = 3

    STATUS_OPTION = ((CAN_SELA, '可售房源'), (CONTROL, '销控房源'),
                     (Sign, '签约房源'), (FULL_MONEY, '全款到账'))

    MOTHER = 0
    NORMAL = 1
    TYPE_OPTION = ((MOTHER, '子母'),
                   (NORMAL, '标准'))

    name = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(default=CAN_SELA, choices=STATUS_OPTION)
    sela_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    is_full_money = models.BooleanField(default=False)
    price = models.CharField(max_length=20, blank=True, null=True)
    floor = models.IntegerField(null=True, blank=True)
    set_type = models.IntegerField(default=NORMAL, choices=TYPE_OPTION)
    count = models.IntegerField(default=1)
    set_num_1 = models.CharField(max_length=20, blank=True, null=True)
    set_num_2 = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'
