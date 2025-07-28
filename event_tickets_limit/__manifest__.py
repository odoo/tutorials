{
    'name': 'event tickets limit',
    'version': '1.0',
    'summary': 'ticket limitation during registration',
    'description': 'Add a ticket limit per registration',
    'author': 'abpa',
    'license': 'LGPL-3',
    'depends': ["event", "website_event"],
    'data': [
        'views/event_ticket_views.xml',
        'views/event_frontend_views.xml',

    ],
    'installable': True,
    'application': True,
}
