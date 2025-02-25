{
    'name': "Event Ticket Limit",
    'version': "1.0",
    'description': """
        Module for limiting the number of tickets that can be booked in single registration.
    """,
    'depends': ['base_setup', 'event' , 'website_event'],
    'category': "Marketing/Events",
    'author': "Himilsinh Sindha (hisi)",
    'website': "https://www.odoo.com/app/events",
    'data': [
        'views/event_ticket_views.xml',
        'views/event_templates_page_registration.xml',
    ],
    'license': "LGPL-3",
    'installable': True,
    'auto_install': True,
}
