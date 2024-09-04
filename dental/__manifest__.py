{
    'name': 'DENTAL',
    'version': '1.2',
    'description': "",
    'depends': [
        'base_setup', 'website', 'account', 'portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dental_views.xml',
        'views/medical_aids_views.xml',
        'views/medical_symptoms_views.xml',
        'views/medication_views.xml',
        'views/patient_history.xml',
        'views/portal_dental_website_views.xml',
        'views/dental_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
