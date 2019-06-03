# Example 6
from datetime import datetime
from functools import wraps
import typing

from validation import validate_type


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


def validate_class_method_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        validate_method_arguments(func, args, kwargs)
        return_value = func(self, *args, **kwargs)
        validate_return(func, return_value)
        return return_value
    return wrapper


class StrongTyping(type):

    @staticmethod
    def _add_attribute(cls, property_name, property_type):
        def set_attribute(self, property_value):
            validate_type(property_type, property_value, property_name)
            setattr(self.__class__, '_' + property_name, property_value)

        def get_attribute(self):
            return getattr(self, '_' + property_name, None)
        setattr(cls, property_name, property(get_attribute, set_attribute))

    def __init__(cls, name, bases, dct):
        # Add decorators to each class method to validate args and return value
        for name, obj in dct.items():
            # Only decorate class methods
            if hasattr(obj, '__call__'):
                setattr(cls, name, validate_class_method_decorator(obj))
        # Validate class attributes - create settter/getter properties
        for key, val in typing.get_type_hints(cls).items():
            StrongTyping._add_attribute(cls, key, val)
        super(StrongTyping, cls).__init__(name, bases, dct)


class Payment(metaclass=StrongTyping):
    """
    Payment object defines funds transfer event.
    """

    def __init__(
            self, amount: float, account_number: int, internal: typing.Optional[bool] = False
    ) -> None:
        self.account_id = '{}_{}'.format('INTERNAL' if internal else 'EXTERNAL', account_number)
        self.amount = amount
        self.timestamp = datetime.now().timestamp()

    def get_status(self, timestamp: datetime) -> str:
        """
        Get payment event status
        """
        return 'PENDING' if self.timestamp > timestamp.timestamp() else 'COMMITTED'


payment = Payment(amount=1.2, account_number=42)
payment.get_status(timestamp=datetime.now())
payment.get_status(timestamp=1)
