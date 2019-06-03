# Example 1
from utils import *

class PaymentProcessor:
    def submit(self, *args, **kwargs):
        pass
payment_processor = PaymentProcessor()


def submit_payment(amount, account_id, reference=None):
    """
    Submit a payment instruction to payment processor queue
    """
    print(
        'Parameter types: account_id - {}, reference - {}, amount- {}'.format(
            type(account_id), type(reference), type(amount)
        )
    )
    # Submit payment to payment processor queue: no feedback if payment is invalid
    payment_processor.submit(account_id, amount, reference)
    return


submit_payment(12.3, 'INTERNAL_123', 'Paying interest')

submit_payment('12.3', 123, 42)
