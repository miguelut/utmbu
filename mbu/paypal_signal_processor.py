from utmbu.settings import PAYPAL_RECEIVER_EMAIL
from mbu.models import PaymentSet
from utmbu import settings
from pprint import pprint
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

__author__ = 'michael'


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != PAYPAL_RECEIVER_EMAIL:
            return

        payment_set = PaymentSet.objects.get(pk=int(ipn_obj.custom))
        payment_set.pp_txn_id = ipn_obj.txn_id
        payment_set.save()

        for payment in payment_set.payments.all():
            payment.status = settings.PAYMENT_PROCESSED
            payment.save()


valid_ipn_received.connect(show_me_the_money)
