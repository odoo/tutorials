{
    'name': "Estate",
    'version': '1.01',
    'depends': ['base'],
    'author': "berm-odoo",
    'category': 'Tutorials',
    'description': "Estate management",
    'license': "LGPL-3",
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True
}
