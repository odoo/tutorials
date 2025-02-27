# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Event Ticket Booking Limit",
    "version": "1.0",
    "author": "Ayush",
    "summary": "Restricts the maximum number of tickets a user can book per registration.",
    "category": "Tutorials/Event Ticket Limit",
    "depends": ["event", "website_event"],
    "data": [
        "views/event_ticket_views.xml",
        "views/event_templates_page_registration.xml"
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
