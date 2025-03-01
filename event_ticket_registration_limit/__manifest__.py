# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Event Ticket Registration Limit",
    'category': 'Events/Ticket',
    'summary': "Restrict the maximum number of tickets that can be booked in a single registration",
    'description': """
    A module to add a feature to restrict the maximum number of tickets per registration
    """,
    'version': "1.0",
    'author': "nees",
    'depends': [
        'website_event'
    ],
    'data': [
        'views/event_ticket_form_view.xml',
        'views/website_ticket_view.xml',
    ],
    'application': True,
    'installable': True,
    'license': "LGPL-3",
}
