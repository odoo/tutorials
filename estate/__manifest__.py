{
    'name': 'Estate',
    'depends':  ['base'],
    'application': True,

    'data': [
        'security/ir.model.access.csv',
        'view/estate_property_views.xml',
        'view/estate_menus.xml',
        'view/estate_property_type_view.xml',
        'view/estate_property_tag_view.xml',
        # 'view/estate_property_offer_view.xml',
        'view/inhertied_user.xml'
    ],
}
