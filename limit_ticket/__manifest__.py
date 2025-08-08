{
    'name': 'Limit Ticket',
    'version': '0.1',
    'summary': 'this will limits the number tickets per registration',
    'description': """
Adds a restriction on ticket bookings per registration.
Limits the number of tickets a user can book.
Enforces validation to prevent exceeding the allowed limit.
    """,
    'author': 'odoo',
    'depends': ['website_event'],
    'data': [
       'views/event_ticket_views.xml',
       'views/event_ticket_registration_views.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
