{
    'name': 'Real Estate',
    'category': 'tutorials',
    'summary': 'Real estate module to sell/rent houses and offices',
    'description': """
    immoweb alias xd
    """,
    'website': 'https://www.odoo.com/app/real_estate',
    'depends': [
        'base_setup',
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_view.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'ibrha',
    'license': 'LGPL-3',
}
