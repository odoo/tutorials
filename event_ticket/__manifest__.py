{
    "name": "Ticket Registration",
    "summary": "Limit events tickets per registration",
    "description": """ The event module allows event organizers to dynamically allot the number of tickets per registration for the events. """,
    "depends": ["website_event"],
    "data": ["views/event_ticket_views.xml" , "views/event_templates_page_registration.xml"],
    "auto_install": True,
    "license": "LGPL-3",
}
