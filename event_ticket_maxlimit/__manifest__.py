# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Event Ticket Limit",
    "version": "1.0",
    'summary': 'Adds a ticket limit per registration in event module',
    "category": "Event/ Event Ticket Limit",
    "description": """
            Adds a ticket limit per registration in `event.event.ticket`.
            Set `tickets_per_registration` to define the limit (0 for no limit).
    """,
    "depends": ["base", "event", "website_event"],
    "data": [
        "views/event_ticket_view.xml",
        "views/event_registration_website_view.xml",
    ],
    "installable": True,
    "auto_install": True,
    "license": "LGPL-3",
}
