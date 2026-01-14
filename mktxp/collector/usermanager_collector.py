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

from mktxp.collector.base_collector import BaseCollector
from mktxp.datasource.usermanager_ds import UserManagerMetricsDataSource

class UserManagerCollector(BaseCollector):
    """ User Manager user traffic metrics data provider collector """
    @staticmethod
    def collect(router_entry):
        if not router_entry.config_entry.user_manager:
            return

        lables = ['user', 'total_uptime', 'total_download', 'total_upload', 'active-sessions']
        records = UserManagerMetricsDataSource.metric_records(router_entry, metric_labels=lables)
        if records:
            lables = ['user']

            for metric in ['total_uptime', 'total_download', 'total_upload']:
                yield BaseCollector.gauge_collector(
                    f'um_{metric}', f'User manager users {metric} statistic', records, metric, lables)
            yield BaseCollector.counter_collector(
                'um_active_sessions', 'User manager active sessions statistic', records, 'active-sessions', lables)
