{
    'name': 'Ticket Limit',
    'version': '1.0',
    'summary': 'Enhancements for the Event app',
    'description': """
        This module adds custom features to the Event app for tutorials.
    """,
    'category': 'Tutorials', 
    'author': 'BHPR',
    'depends': ['event'], 
    'data': [
        'views/event_views.xml',
    ],
    'application': True,  
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
