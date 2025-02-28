{
    'name': "Ticket Limit",
    'version': "1.0",
    'summary': 'Enhancements for the Event app',
    'description': """
        This module adds custom features to the Event app for tutorials.
    """,
    'category': "Tutorials", 
    'author': "BHPR",
    'depends': ['website_event'], 
    'data': [
        'views/event_event.xml',
        'views/event_ticket_registration.xml'
    ],
    'auto_install': True,
    'license': 'LGPL-3',
}
