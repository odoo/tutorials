{
    "name": "Appointment Capacity Management",
    "version": "1.0",
    "summary": "Enhance appointment booking with multiple bookings and seats per slot.",
    "description": """
        - Allows multiple bookings per time slot.
        - Supports multiple seats per slot.
    """,
    "author": "Darshan Patel",
    "depends": ["appointment", "appointment_account_payment", "calendar"],
    "data": [
        "views/appointment_type_views.xml",
        "views/appointment_template_appointment.xml",
        "views/calendar_event_views.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
