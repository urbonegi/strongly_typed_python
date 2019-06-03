# Example 5
import typing

from validation import validate_type


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
        # class attribute validation - create settter/getter prop
        for key, val in typing.get_type_hints(cls).items():
            StrongTyping._add_attribute(cls, key, val)
        super(StrongTyping, cls).__init__(name, bases, dct)


class Payment(metaclass=StrongTyping):
    """
    Payment object defines funds transfer event.
    """
    amount: float
    account_id: str

    def __init__(
            self, amount: float, account_number: int, internal: bool
    ) -> None:
        self.account_id = '{}_{}'.format('INTERNAL' if internal else 'EXTERNAL', account_number)
        self.amount = amount

    def __repr__(self) -> str:
        return 'Account ID: {}, type ({}); amount: {}, type ({}).'.format(
            self.account_id, type(self.account_id),
            self.amount, type(self.amount)
        )


payment = Payment(amount=1.2, account_number=123, internal=True)
print(payment.account_id, type(payment.account_id))
payment.account_id = 123
