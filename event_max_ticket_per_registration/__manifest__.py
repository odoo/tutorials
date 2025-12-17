{
    'name': "Event Limit Max tickets",
    'version': '1.0',
    'depends': ['website_event'],
    'author': "Rishav Shah",
    'category': 'events',
    'description': """
    Limit maximum number of tickets per registration
    """,
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'data': [
        'views/event_event_views.xml',
        'views/event_templates_page_registration.xml',
    ],
}
