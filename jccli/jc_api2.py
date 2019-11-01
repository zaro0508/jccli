# -*- coding: utf-8 -*-

"""
.. currentmodule:: jccli.jc_api2.py
.. moduleauthor:: zaro0508 <zaro0508@gmail.com>

This is a utility library for the jumpcloud version 2 api

.. note::

    To learn more about the jumpcloud api 2
    `project website <https://github.com/TheJumpCloud/jcapi-python/tree/master/jcapiv2>`_.
"""
import jcapiv2
from jcapiv2.rest import ApiException

from jccli.helpers import class_to_dict

class jc_api2:
    """
        Wrapper for Jumpcloud API v2
    """
    def __init__(self, api_key):
        configuration = jcapiv2.Configuration()
        configuration.api_key['x-api-key'] = api_key
        self.graph_api = jcapiv2.GraphApi(jcapiv2.ApiClient(configuration))
        self.groups_api = jcapiv2.GroupsApi(jcapiv2.ApiClient(configuration))
        self.bulk_job_requests_api = jcapiv2.BulkJobRequestsApi(jcapiv2.ApiClient(configuration))

    def bind_user_to_group(self, user_id, group_id):
        """
        Associates a jumpcloud user to a jumpcloud group
        :param user_id:
        :param group_id:
        :return:
        """
        group_id = group_id
        content_type = 'application/json'
        accept = 'application/json'
        body = jcapiv2.UserGroupMembersReq(id=user_id,
                                           op="add",
                                           type="user")
        x_org_id = ''

        try:
            # Manage the associations of a User Group
            api_response = self.graph_api.graph_user_group_members_post(group_id,
                                                                        content_type,
                                                                        accept,
                                                                        body=body,
                                                                        x_org_id=x_org_id)
            return api_response
        except ApiException as error:
            raise "Exception when calling GraphApi->graph_user_group_members_post: %s\n" % error

    def bind_ldap_to_user(self, ldap_id):
        """
        Associates a jumpcloud user to a jumpcloud LDAP
        :param ldap_id:
        :return:
        """
        ldapserver_id = ldap_id
        content_type = 'application/json'
        accept = 'application/json'
        body = jcapiv2.GraphManagementReq()
        x_org_id = ''

        try:
            # Manage the associations of a LDAP Server
            api_response = self.graph_api.graph_ldap_server_associations_post(ldapserver_id,
                                                                              content_type,
                                                                              accept,
                                                                              body=body,
                                                                              x_org_id=x_org_id)
            return api_response
        except ApiException as error:
            raise "Exception when calling \
                   GraphApi->graph_ldap_server_associations_post: %s\n" % error

    def get_group_id(self, group_name, limit=10):
        # pylint: disable-msg=too-many-locals
        """
        Get the jumpcloud group id from a jumpcloud group name
        :param group_name:
        :param limit:
        :return:  The jumpcloud group id otherwise NONE if not found.
        """
        content_type = 'application/json'
        accept = 'application/json'
        fields = ['[]']
        filter = ['[]']
        limit = 10
        skip = 0
        sort = ['[]']
        x_org_id = ''

        group_id = None
        try:
            # List All Groups
            results = self.groups_api.groups_list(content_type,
                                                  accept,
                                                  fields=fields,
                                                  filter=filter,
                                                  limit=limit,
                                                  skip=skip,
                                                  sort=sort,
                                                  x_org_id=x_org_id)

            groups = class_to_dict(results)

            for group in groups:
                if group['_name'] == group_name:
                    group_id = group['_id']

            return group_id
        except ApiException as error:
            raise "Exception when calling GroupsApi->groups_list: %s\n" % error
