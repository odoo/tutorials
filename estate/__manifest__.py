{
    'name': 'RealEstate',
    'version': '1.0',
    'category': 'Real Estate/Brokerage',
    'summary': 'A module to manage real estate advertisements and property offers',
    'description': """A simple module to manage real estate ads.List your properties, track details like bedrooms and garden,let buyers make offers, and accept or reject them.""",
    'author': 'Pranjali Sangavekar(prsan)',
    'license': 'LGPL-3',
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
}
