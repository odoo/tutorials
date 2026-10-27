# -*- coding: utf-8 -*-

import logging
import random

from odoo import http
from odoo.http import request

logger = logging.getLogger(__name__)

_item_providers = []


def register_dashboard_items_provider(fn):
    _item_providers.append(fn)
    return fn


@register_dashboard_items_provider
def _base_items(http_request):
    """Built-in items for the Awesome Dashboard."""
    return [
        {
            'comp': 'numb',
            'label': 'New orders this month',
            'value': random.randint(10, 200),
        },
        {
            'comp': 'numb',
            'label': 'Total amount this month',
            'value': random.randint(100, 1000),
        },
        {
            'comp': 'numb',
            'label': 'Average t-shirts per order this month',
            'value': random.randint(4, 12),
        },
        {
            'comp': 'numb',
            'label': 'Cancelled orders this month',
            'value': random.randint(0, 50),
        },
        {
            'comp': 'numb',
            'label': 'Average time from new to sent or cancelled (hours)',
            'value': random.randint(4, 123),
        },
        {
            'comp': 'chart',
            'label': 'T-shirts sold by size',
            'size': 2,
            'data': {
                's': random.randint(0, 150),
                'm': random.randint(0, 150),
                'xl': random.randint(0, 150),
            },
        },
    ]


class AwesomeDashboard(http.Controller):
    @http.route('/awesome_dashboard/statistics', type='jsonrpc', auth='user')
    def get_statistics(self):
        """Return the statistics displayed in the dashboard, merged from
        every module that registered items providers."""
        return {
            'data': [
                item
                for provider in _item_providers
                for item in provider(request)
            ],
        }
