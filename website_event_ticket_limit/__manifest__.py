{
    'name': "Events Ticket Limit",
    'version': "1.0",
    'category': 'Marketing/Events',
    'sequence': 140,
    'summary': 'Publish events, sell tickets, ticket limit',
    'depends': [
        'event',
        'website_event'
    ],
    'data': [
        'views/event_event_view.xml',
        'views/event_registration_ticket_limit.xml'
    ],
    'license': 'LGPL-3',
}
