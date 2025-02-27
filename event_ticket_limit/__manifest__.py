# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Limit event tickets",
    'description': "Limits the number of tickets per user registration",
    'version': '1.0',
    'author': "nmak",
    'depends': ["event", "website_event"],
    'data': [
        'views/event_ticket_form_view.xml',
        'views/website_ticket_view.xml'
    ],
    'installable': True,
    'license': "LGPL-3",
}
