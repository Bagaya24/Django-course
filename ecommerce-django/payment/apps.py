from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'

    # Set up PayPal IPN signal
    def ready(self):
        import payment.hooks
