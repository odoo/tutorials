{
    "name":'Real Estate',
    "summary": "An estate app",
    'category':'Real Estate/Brokerage',
    'depends': ['base','mail'],
    'author': 'Devmitra sharma (dvsh)',
    'data':[
        'security/estate_security.xml',
        'security/ir.model.access.csv',
        'views/estate_property_tags_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_res_users.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'demo':[
        'demo/estate_property_type_demo.xml',
        'demo/estate_property_tag_demo.xml',
        'demo/estate_property_demo.xml',
        'demo/estate_property_offer_demo.xml'
        ],
    'assets': {
        'web.assets_backend':   [
            'estate/static/description/icon.png',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    "license":"LGPL-3"
}
