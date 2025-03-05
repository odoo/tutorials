{
    "name": "Limit Tickets Per Registration",
    "summary": "Limit the Number of Tickets Per Registration (pmah)",
    "description": "Restricts the maximum number of tickets a user can register for an event (pmah)",
    "version": "0.1",
    "depends": ["website_event"],
    "auto_install": True,
    "license": "AGPL-3",
    "data": [
        "views/event_ticket_views.xml",
        "views/event_templates_page_registration.xml"
    ],
}
