#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.cli
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is the entry point for the command-line interface (CLI) application.  It
can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.
"""
import logging
import click

from .__init__ import __version__
from jccli.helpers import get_users_from_file
from jccli.jc_api1 import jc_api1
from jccli.jc_api2 import jc_api2

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """
    An information object to pass data between CLI functions.
    """

    def __init__(self):  # Note: This object must have an empty constructor.
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """
    Run jccli.
    """
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose

@cli.command()
def version():
    """
    Get the library version.
    """
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@click.option('--key', required=True, type=str, help='Jumpcloud API key')
@click.option('--users', required=True, type=str, help='Path to the users file')
@pass_info
def sync(_: Info, key, users):
    """
    Sync users to jumpcloud.
    """
    click.echo("Sync users on jumpcloud with users in " + users)
    sync(key, users)


def sync(key, users_file):
    api1 = jc_api1(key)
    api2 = jc_api2(key)

    jc_usernames=[]
    jc_emails=[]
    jc_users=[]
    jc_users_request = api1.get_users(limit='')
    if jc_users_request:
        for jc_user in jc_users_request:
            jc_usernames.append(jc_user['_username'])
            jc_emails.append(jc_user['_email'])
            jc_users.append({'username':jc_user['_username'], 'email':jc_user['_email']})

    click.echo("jumpcloud users: " + ','.join(jc_usernames))

    click.echo("getting users from file: " + users_file)
    users = get_users_from_file(users_file)
    if users is None:
        exit("No users to manage therefore nothing to do")

    # create new users
    added_users=[]
    for user in users:
        do_create_user = False
        try:
            user_name = user['username']
            user_email = user['email']
            if (user_name not in jc_usernames) and (user_email not in jc_emails):
                do_create_user = True
            else:
                click.echo(user_name + " user already exists")
        except KeyError as e:
            raise e

        if do_create_user:
            click.echo("creating user: " + user_name)
            # response = api1.create_user(user_name, user_email, user['firstname'], user['lastname'])
            # if response is not None:
            #     added_users.append({'username':user_name, 'email':user_email})
            added_users.append({'username':user_name, 'email':user_email})
            group_id = api2.get_group_id("staff")
            if group_id:
                user_id = api1.get_user_id(user_name)
                click.echo("binding " + user_id + " to group: " + group_id)
                # api2.bind_user_to_group(user_id, group_id)

    # remove users that do not exist in the users file
    local_usernames=[]
    local_emails=[]
    for user in users:
        local_usernames.append(user['username'])
        local_emails.append(user['email'])

    removed_users=[]
    for jc_user in jc_users:
        do_remove_user = False
        user_name = jc_user['username']
        user_email = jc_user['email']
        if (user_name not in local_usernames) and (user_email not in local_emails):
            do_remove_user = True

        if do_remove_user:
            click.echo("removing user: " + user_name)
            removed_users.append(jc_user)
