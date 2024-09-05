{
    'name': 'DENTAL',
    'version': '1.2',
    'description': "",
    'depends': [
        'base_setup', 'website',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'views/portal_template.xml',
        'views/tag_views.xml',
        'views/medical_history_views.xml',
        'views/dental_views.xml',
        'views/medical_aids_views.xml',
        'views/medical_symptoms_views.xml',
        'views/medication_views.xml',
        'views/dental_menu.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
