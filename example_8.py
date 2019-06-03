from example_7 import *


class TypedTuple(tuple, metaclass=StrongTyping):
    """
    Fixed type tuple
    """

    def __new__(
            cls, iterable: Type(typing.Optional[typing.Iterable[str]], "Iterable of type str") = ()
    ) -> Type(typing.Tuple[str, ...], "Tuple of any length with items of str type"):
        return super().__new__(cls, iterable)


print(TypedTuple())
print(TypedTuple(['1', '2']))
print(TypedTuple.__new__.__doc__)
TypedTuple([1, 2])
