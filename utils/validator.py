"""Validation helpers."""

import re


class Validator:
    EMAIL_RE = re.compile(
        r"^[A-Z0-9._%+-]+@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}$",
        re.IGNORECASE,
    )
    USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,30}[A-Za-z0-9])?$|^[A-Za-z0-9]$")

    @classmethod
    def is_valid_email(cls, email):
        return bool(email and cls.EMAIL_RE.match(email.strip()))

    @classmethod
    def is_valid_username(cls, username):
        return bool(username and cls.USERNAME_RE.match(username.strip()))
