{
    'name': "Event Registration limit",
    'category': "Marketing/Events",
    'summary': "Module to Limit the Number of Tickets Per Registration",
    'depends': ['event' , 'website_event'],
    'data': [
        'views/event_event_views.xml',
        'views/event_registration_views.xml'
    ],
    'installable': True,
    'license': "AGPL-3",
}
