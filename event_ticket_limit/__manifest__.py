{
    "name": "Event Ticket Limit",
    "summary": """
        Module for limiting the number of tickets per registration
    """,
    "description": """
        Module for limiting the number of tickets per registration
    """,
    "author": "Odoo",
    "website": "https://www.odoo.com",
    "category": "Event/ Event Ticket Limit",
    "version": "0.1",
    "installable": True,
    "auto_install": True,
    "depends": ["base_setup", "event", "website_event"],
    "data": [
        "views/event_tickets_views.xml",
        "views/event_registration_website_view.xml",
    ],
    "license": "AGPL-3",
}
