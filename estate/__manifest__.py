{
    'name': 'Real Estate',
    'category': 'Tutorials/RealEstate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'summary': 'Help users with Real estate.',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml'
    ],  
    'demo': [
        'demo/estate_property_tag.xml',
        'demo/estate_property_type.xml',
        'demo/estate_partners.xml',
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml'
    ]  
}
