{
    'name': "real.estate",
    'summary': "summary of the real estate",
    'description': """Rugot first module""",
    'author': "Ruchita Gothi (Rugot)",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/properties_views.xml',
        'views/real_estate_tag.xml',
        'views/real_estate_properties_offer.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
