# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.errors.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

Exceptions

"""

class SystemUserNotFoundError(Exception):
# pylint: disable=
    """
    Jumpcloud system user is not found
    """
    pass

class MissingRequiredArgumentError(Exception):
    """
    Required arguments are missing
    """
    pass
