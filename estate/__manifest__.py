{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Odoo S.A. (aykar)",
    'category': 'Customizations',
    'description': """
    This module is designed to manage real estate properties, including details such as property type, location, price, and status.
    
    It allows users to easily track and organize their real estate assets, making it easier to manage and analyze their property portfolio.
    """,
    'installable': True,
    'application': True,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
}
