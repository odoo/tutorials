{
    'name': 'Health',
    'version': '1.0',
    'category': 'Tutorials',
    'Summary': 'Health and Patient Appointment System',
    'description': 'Manage your appointments',
    'application': True,
    'installable': True,
    'author': 'times',
    'website': 'https://www.odoo.com/app/health',
    'depends': ['base'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/health_patient_views.xml',
        'views/health_appointment_views.xml',
        'views/health_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'health/static/src/components/rating_widget/rating_widget.js',
            'health/static/src/components/rating_widget/rating_widget.xml',
        ]
    }
}
