import unittest
import functools


def tag_error(func):
    """Decorates a unittest test function to add failure information to the TestCase."""

    @functools.wraps(func)
    def decorator(self, *args, **kwargs):
        """Add failure information to `self` when `func` raises an exception."""
        self.test_failed = False
        try:
            func(self, *args, **kwargs)
        except unittest.SkipTest:
            raise
        except Exception:  # pylint: disable=broad-except
            self.test_failed = True
            raise  # re-raise the error with the original traceback.

    return decorator
