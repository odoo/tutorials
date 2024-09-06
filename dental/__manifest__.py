{
    'name': 'DENTAL',
    'version': '1.2',
    'description': "",
    'depends': [
        'base', 'website',
        'mail', 'account'
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/dental_data.xml',
        'data/dental_tags.xml',

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
