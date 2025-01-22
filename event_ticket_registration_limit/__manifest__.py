{
    'name': 'Event Ticket Registration Limit',
    'description': 'adds a feature to restrict the maximum number of tickets per registration',
    'category': 'Event/Event Ticket',
    'depends': ['base', 'event', 'website_event'],

    'version': '1.0',
    'author': 'Kishan B. Gajera',

    'installable': True,
    'application': True,

    'license': 'LGPL-3',

    'data': [
        'views/event_ticket_view.xml',
        'views/modal_ticket_registration_web_view.xml',
    ]
}
