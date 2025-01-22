{
    "name": "Event Ticket Limit",
    "category": "Event/ Event Ticket Limit",
    "summary": """
The purpose of this module is to implement a functionality for limiting the number of tickets per registration.
You can limit the number of tickets per registration by setting the tickets_per_registration field in the event.event.ticket model.
If value is set to 0, then there is no limit on the number of tickets per registration.
""",
    "version": "1.0",
    "depends": ["base_setup", "event", "website_event"],
    "data": [
        "views/event_tickets_views.xml",
        "views/event_registration_website_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
}
