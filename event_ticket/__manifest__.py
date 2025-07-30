{
    'name': "Event Tickets",
    'version': "1.0",
    'category': "Events",
    'summary': "Manage event tickets and registrations",
    'description': "The event module allows event organizers to dynamically allot the number of tickets per registration for the events.",
    'author': "sujal_asodariya",
    'depends': ["website_event"],
    'data': [
        "views/event_register_website_views.xml",
        "views/event_ticket_views.xml",
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3",
}
