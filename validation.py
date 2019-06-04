from typing import Iterable, Tuple, Union


def _validate_type(expected_type, given_value):
    # TODO validate Dict
    if expected_type == type(given_value):
        return True
    elif expected_type.__class__ == Union.__class__:
        if any(
            _validate_type(tp, given_value) for tp in expected_type.__args__
        ):
            return True
    elif issubclass(expected_type, Tuple) and isinstance(given_value, tuple):
        if len(expected_type.__args__) > 1 and expected_type.__args__[1] == Ellipsis:
            # Tuple of any length of elements with same type
            if all(
                _validate_type(expected_type.__args__[0], value) for value in given_value
            ):
                return True
        else:
            # Fixed length tuple
            if len(given_value) == len(expected_type.__args__) and \
                    all(
                        _validate_type(
                            val, given_value[index]
                        ) for index, val in enumerate(expected_type.__args__)
                    ):
                return True
    elif issubclass(expected_type, Iterable) and isinstance(given_value, Iterable):
        if all(
            _validate_type(expected_type.__args__[0], i) for i in given_value
        ):
            return True
    return False


def validate_type(expected_type, given_value, property_name):
    if not _validate_type(expected_type, given_value):
        raise TypeError(
            'Attribute `{}` value - `{}` does not match '
            'type declared in annotations - {}.'.format(
                property_name,
                given_value,
                expected_type
            )
        )
