from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
import time

from . import models

@receiver(valid_ipn_received)
def paypal_payment_receive(sender, **kwargs):
    # Grab the info that PayPal sends
    # Add 5 sec pause for PayPal to send IPN data
    time.sleep(5)

    paypal_obj = sender
    my_invoice = str(paypal_obj.invoice)

    # Match the PayPal invoice to the Order invoice
    my_order = models.Order.objects.get(invoice=my_invoice)
    # Record that the order was paid
    my_order.paid = True
    my_order.save()