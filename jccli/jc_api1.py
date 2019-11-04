# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.jc_api1.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a utility library for the jumpcloud version 1 api

.. note::

    To learn more about the jumpcloud api 1
    `project website <https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv1>`_.
"""
import jcapiv1
from jcapiv1.rest import ApiException

from jccli.helpers import class_to_dict

# pylint: disable=too-many-arguments
class jc_api1:
    """
        Wrapper for Jumpcloud API v1
    """
    def __init__(self, api_key):
        configuration = jcapiv1.Configuration()
        configuration.api_key['x-api-key'] = api_key
        self.system_users_api = jcapiv1.SystemusersApi(jcapiv1.ApiClient(configuration))

    def get_users(self, limit=10, skip=0, search='', filter='', sort='', fields=''):
        """
        Get users from jumpcloud
        :param limit:
        :param skip:
        :param search:
        :param filter:
        :param sort:
        :param fields:
        :return: a list of users with dict of settings
        """
        content_type = 'application/json'
        accept = 'application/json'
        limit = limit
        skip = skip
        sort = sort
        fields = fields
        x_org_id = ''
        search = search
        filter = filter

        try:
            api_response = self.system_users_api.systemusers_list(content_type,
                                                                  accept,
                                                                  limit=limit,
                                                                  skip=skip,
                                                                  sort=sort,
                                                                  fields=fields,
                                                                  x_org_id=x_org_id,
                                                                  search=search,
                                                                  filter=filter)
            users = class_to_dict(api_response.results)
            return users
        except ApiException as error:
            raise "Exception when calling SystemusersApi->systemusers_list: %s\n" % error

    def create_user(self, username, email, firstname=None, lastname=None):
        """
        Create a new user
        :param username:
        :param email:
        :param firstname:
        :param lastname:
        :return: Create a new user in jumpcloud
        """
        content_type = 'application/json'
        accept = 'application/json'
        x_org_id = ''
        body = jcapiv1.Systemuserputpost(username=username,
                                         email=email,
                                         firstname=firstname,
                                         lastname=lastname,
                                         sudo=True,
                                         allow_public_key=True)
        try:
            api_response = self.system_users_api.systemusers_post(content_type,
                                                                  accept,
                                                                  body=body,
                                                                  x_org_id=x_org_id)
            return api_response
        except ApiException as error:
            raise "Exception when calling SystemusersApi->systemusers_post: %s\n" % error

    def get_user_id(self, username):
        """
        Get the jumpcloud user id from the user name
        :param username
        :return:  the user id
        """
        users = self.get_users(limit='', fields="username")

        user_id = None
        for user in users:
            if user['_username'] == username:
                user_id = user['_id']

        return user_id
