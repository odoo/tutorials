{
    'name': "Ticket Limiter",
    'version': '1.0',
    'author': "Sufiyan Shaikh",
    'installable': True,
    'description': "Limits the number of tickets per user",
    'depends': ['website_event'],
    'data': [
        'views/event_ticket_view.xml',
        'views/event_templates_page_registration.xml',
    ],
    'license': 'LGPL-3',
}
