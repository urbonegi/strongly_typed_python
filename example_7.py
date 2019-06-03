# Example 7
from datetime import datetime
from functools import wraps
import typing

from validation import validate_type


def validate_method_arguments(func, args, kwargs):
    types_dict = func.__annotations__.copy()
    types_dict.pop('return', None)
    # Validate argument types
    for index, (attr, attr_type) in enumerate(types_dict.items()):
        if attr in kwargs:
            validate_type(attr_type.type, kwargs[attr], attr)
        elif len(args) - 1 >= index:
            validate_type(attr_type.type, args[index], attr)
        else:
            validate_type(attr_type.type, None, attr)


def validate_return(func, return_value):
    types_dict = func.__annotations__
    return_type = types_dict['return']
    # Validate return type
    if return_value:
        validate_type(return_type.type, return_value, 'return_value')


def extend_docstring(type_annot, spaces=4):
    docs = []
    docs.extend(
        (':param {}: {}'.format(attr, attr_type.description)
         for (attr, attr_type) in type_annot.items() if attr != 'return')
    )
    docs.extend(
        (':type {}: {}'.format(attr, attr_type.type)
         for (attr, attr_type) in type_annot.items() if attr != 'return')
    )
    # Add return type if exist
    if 'return' in type_annot:
        docs.extend([':return: {}'.format(type_annot['return'].description),
                     ':rtype: {}'.format(type_annot['return'].type)])
    return ('\n' + ' ' * spaces).join(docs)


class Type:
    def __init__(self, type, description=None):
        self.description = description
        self.type = type


def add_function_docs(wrapper, func):
    type_annot = func.__annotations__
    func_doc = func.__doc__ or '\n        '
    wrapper.__doc__ = func_doc + extend_docstring(type_annot, spaces=8)
    return wrapper


def validate_class_method_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        validate_method_arguments(func, args, kwargs)
        return_value = func(self, *args, **kwargs)
        validate_return(func, return_value)
        return return_value
    return add_function_docs(wrapper, func)


class StrongTyping(type):

    @staticmethod
    def _add_attribute(cls, property_name, property_type):
        def set_attribute(self, property_value):
            validate_type(property_type.type, property_value, property_name)
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

    def __new__(cls, name, bases, clsdict):
        type_annot = clsdict.get('__annotations__', {})
        class_doc = clsdict.get('__doc__', '\n    ')
        clsdict['__doc__'] = class_doc + extend_docstring(type_annot)
        # Extend doc-strings
        return super(StrongTyping, cls).__new__(cls, name, bases, clsdict)


class Payment(metaclass=StrongTyping):
    """
    Payment object defines funds transfer event.
    """
    amount: Type(float, "Payment amount")
    account_id: Type(str, "Target account ID")
    timestamp: Type(float, "Payment timestamp")

    def __init__(self, amount: Type(float, "Payment amount"),
                 account_number: Type(int, "Target account number"),
                 internal: Type(bool, "Is account internal or external?")) -> Type(None, ""):
        """
        Payment object constructor method
        """
        self.account_id = '{}_{}'.format('INTERNAL' if internal else 'EXTERNAL', account_number)
        self.amount = amount
        self.timestamp = datetime.now().timestamp()

    def get_status(
            self, timestamp: Type(datetime, "Payment validation timestamp")
    ) -> Type(str, "Payment status at given timestamp"):
        """
        Get payment event status
        """
        return 'PENDING' if self.timestamp > timestamp.timestamp() else 'COMMITTED'


print(Payment.__doc__)
print(Payment.__init__.__doc__)
print(Payment.get_status.__doc__)
