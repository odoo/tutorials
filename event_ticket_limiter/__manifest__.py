{
    'name': 'Event Ticket Limiter',
    'version': '1.0',
    'description': 'This module restricts the number of event registrations a user can make from the website in Odoo. It ensures controlled ticket distribution and prevents excessive bookings.',
    'license': 'LGPL-3',
    'category': 'Events/Event Ticket Limiter',
    'depends': [
        'event',
        'website_event'
    ],
    'data': [
        'views/event_ticket_views.xml',
        'views/event_template_page_registration.xml',
    ],
    'auto_install': True,
    'installable': True
}
