{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Tutorial',
    'summary': 'Manage estate properties',
    'author': 'Omar',
    'application': True,
    'depends': ['base'],  
 'data': [
        'security/ir.model.access.csv',  # Add access rights
                'views/estate_property_views.xml',  # Add the XML file

    ],

    'installable': True,
}
