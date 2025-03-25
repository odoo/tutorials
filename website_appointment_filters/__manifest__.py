# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Website Appointment Filters",
    'category': 'Services/Appointment',
    'summary': "Added filters on search domain",
    'description': """
    A module to add filters in Website View for appointments
    """,
    'version': "1.0",
    'author': "nees",
    'depends': [
        'website_appointment',
        'appointment_account_payment'
    ],
    'data': [
        'views/appointment_filter_templates.xml'
    ],
    'application': True,
    'installable': True,
    'license':"LGPL-3",
}
