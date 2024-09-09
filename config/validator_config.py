from config.log_config import logger as log
from typing import TypeVar, Generic
import re

T = TypeVar("T")


class Validator(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.errors = []

    def add_rule(self, rule: T, message: str):
        if not rule(self.value):
            self.errors.append(message)
        return self

    def add_regex_rule(self, pattern, message):
        return self.add_rule(lambda x: re.match(pattern, x), message)

    def is_valid(self):
        return not bool(self.errors)

    def validate(self):
        if self.errors:
            for error in self.errors:
                log.error(error)
                raise ValueError(error)

        return self.value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other and \
            self.errors == other.errors
