{
    'name': 'Website Appointment Filters',
    'version': '1.0',
    'depends': ['base', 'website_appointment', 'appointment_account_payment'],
    'author': 'Kishan B. Gajera',
    'category': 'Appointment',
    'description': """
        A sample module to add filters in Appointment Website View
    """,

    'application': True,
    'installable': True,

    'data': [
        'views/appointment_templates_appointment_filters.xml'
    ],

    'license':'LGPL-3',
}
