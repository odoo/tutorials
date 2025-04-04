{
    'name': 'Appointment update',
    'version': '1.0',
    'description': """
Allow clients to Schedule Appointments through the Portal and book multiple appointment
    """,
    'depends': ['appointment', 'appointment_account_payment', 'website_appointment'],
    'data': [
        'views/appointment_update_type_views.xml',
    ],
    'installable': True,
    'license': 'OEEL-1',
}
