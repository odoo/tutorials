# -*- encoding: utf-8 -*-
{
    'name': 'Event ticket max register',
    'version': '1.0',
    'summary': 'Event ticket max registertion per user',
    'depends': ['base', 'event', 'website_event'],
    'data': [
        'views/event_ticket_limit_view.xml',
        'views/event_frontend_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
