{
    'name': 'Estate',
    #'version': '1.0',
    # 'category': 'Tutorial',
    # 'summary': 'Manage estate properties',
    # 'author': 'Omar',
    'depends': ['base','sale'],  
 'data': [
        'security/ir.model.access.csv',  # Add access rights
        'views/estate_property_views.xml',  # Add the XML file
        'views/estate_menus.xml',  # Add the XML file

    ],
    'application': True,

    'installable': True,
}
