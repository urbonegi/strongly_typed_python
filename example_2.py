# Example 2
import typing

from utils import *

def submit_payment(
        amount: float, account_id: str, reference: typing.Optional[str] = None
) -> None:
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


print(typing.get_type_hints(submit_payment))
submit_payment('12.3', 123, 42)
