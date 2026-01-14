# coding=utf8
## Copyright (c) 2020 Arseniy Kuznetsov
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.


from mktxp.datasource.base_ds import BaseDSProcessor
from mktxp.utils.utils import parse_mkt_uptime


class UserManagerMetricsDataSource:
    """ User Manager user traffic metrics data provider """
    @staticmethod
    def metric_records(router_entry, *, metric_labels=None):
        translation_table = {
            'total_uptime': lambda value:  parse_mkt_uptime(value)
        }
        if metric_labels is None:
            metric_labels = ['user', 'total_uptime', 'total_download', 'total_upload', 'active-sessions']

        try:
            router_resource = router_entry.api_connection.router_api().get_resource('/user-manager/user/')
            users = router_resource.get()
            user_stats = router_resource.call('monitor', {'numbers': ','.join(u['id'] for u in users), 'once': ''})
            for index, stat in enumerate(user_stats):
                stat['user'] = users[index]['name']

            return BaseDSProcessor.trimmed_records(router_entry, router_records=user_stats,
                                                   metric_labels=metric_labels, translation_table=translation_table)
        except Exception as exc:
            print(
                f'Error getting system resource info from router {router_entry.router_name}@{router_entry.config_entry.hostname}: {exc}')
            return None
