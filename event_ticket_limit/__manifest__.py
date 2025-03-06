{
    'name' : "Event Ticket Limit",
    'version' : "1.0",
    'category': "Marketing/Events",
    'summary' : "Module to Limit the Number of Tickets Per Registration",
    'description': """
        This module restricts the number of tickets that can be booked in a single registration.
        The default limit was 9, but this module enforces a new configurable limit.
    """,
    'depends' : ['event' , 'website_event'],
    'data' : [
        'views/event_event_views.xml',
        'views/event_registration_views.xml'
    ],
    'installable' : True,
    'license': 'AGPL-3',
}
