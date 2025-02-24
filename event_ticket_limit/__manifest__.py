{
    'name': "Event Ticket Limit",
    'description': """
    Limit the number of tickets per registration
    """,
    'version': '1.0',
    'depends': ['event', 'website_event'],
    'author': "Prince Beladiya",
    'license': 'LGPL-3',
    'installable': True,
    'data': [
        'views/event_ticket_template_views.xml',
        'views/event_ticket_views.xml',
        'views/res_config_settings_views.xml'
    ]
}
