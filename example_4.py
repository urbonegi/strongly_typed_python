# Example 4
from functools import wraps
import typing

from utils import *
from validation import validate_type


def validate_function_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        validate_method_arguments(func, args, kwargs)
        return_value = func(*args, **kwargs)
        validate_return(func, return_value)
        return return_value
    return wrapper


def validate_method_arguments(func, args, kwargs):
    # typing.get_type_hints return example from before:
    # {'amount': <class 'float'>, 'account_id': <class 'str'>,
    # 'reference': typing.Union[str, NoneType], 'return': <class 'NoneType'>}
    types_dict = typing.get_type_hints(func)
    types_dict.pop('return', None)
    # Validate argument types
    for index, (attr, attr_type) in enumerate(types_dict.items()):
        if attr in kwargs:
            validate_type(attr_type, kwargs[attr], attr)
        elif len(args) - 1 >= index:
            validate_type(attr_type, args[index], attr)
        else:
            validate_type(attr_type, None, attr)


def validate_return(func, return_value):
    types_dict = typing.get_type_hints(func)
    return_type = types_dict['return']
    # Validate return type
    if return_value:
        validate_type(return_type, return_value, 'return_value')


@validate_function_decorator
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
    return 1


submit_payment(12.3, 'INTERNAL_123', 'Paying interest')
