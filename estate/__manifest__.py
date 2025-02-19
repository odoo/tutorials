
{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo S.A.",
    'category': 'Category',
    'description': "Description text",
    'website': 'https://www.odoo.com/page/estate',
    'license': 'LGPL-3',

    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
        
    ],
    'application': True,
    'installable': True
}
