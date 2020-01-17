import logging
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime

from .models import AlipayCode
from .tasks import deal_overdue


logger = logging.getLogger(__name__)


@receiver(post_save, sender=AlipayCode, dispatch_uid='transaction_follow_up')
def transaction_follow_up(sender, instance, created, **kwargs):
    alipayaccount = instance.alipay_account
    if instance.status == 1:
        expired_in_minutes = alipayaccount.expired_in if alipayaccount else 5
        deal_overdue.apply_async((instance.id,),
                                 eta=localtime() + timedelta(minutes=expired_in_minutes))
