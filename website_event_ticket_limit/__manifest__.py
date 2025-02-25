
{
    'name': 'Events Ticket Limit',
    'version': '1.4',
    'category': 'Marketing/Events',
    'sequence': 140,
    'summary': 'Publish events, sell tickets, ticket limit',
    'website': 'https://www.odoo.com/app/events',
    'depends': [
        'event',
        'website',
        'website_partner',
    ],
    'data': [
        'views/event_registration_ticket_limit.xml'
    ],
    'license': 'LGPL-3',
}
