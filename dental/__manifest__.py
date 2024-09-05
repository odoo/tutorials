{
    'name': 'dental',
    'version': '1.0',
    'description': "Dental Care",
    'category': 'website',
    'author': 'YASP',
    'website': 'https://www.yourcompany.com',
    'sequence': 1,
    'summary': 'Dental management',
    'depends': [
        'base', 'website', 'portal', 'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dental_portal_templates.xml',
        'views/portal_my_dental.xml',
        'views/dental_views.xml',
        'views/medical_aids_views.xml',
        'views/medical_symptoms_views.xml',
        'views/medication_views.xml',
        'views/dental_patient_history_views.xml',
        'views/dental_menu.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
