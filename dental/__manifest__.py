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
        'base', 'website'
    ],
    'data': [
        'security/ir.model.access.csv',
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
