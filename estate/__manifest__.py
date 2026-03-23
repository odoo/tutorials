{
    'name': 'estate',
    'author': 'qugeo',
    'depends': ['base'],
    'application': True,
    'license': 'LGPL-3',

    'data' : [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',

        'views/estate_menus.xml',

        'views/estate_property_view_list.xml',
        'views/estate_property_view_form.xml',
        'views/estate_property_view_search.xml',

        'views/estate_property_type_view_form.xml',

        'views/estate_property_tag_view_form.xml',

        'views/estate_property_offer_view_list.xml',
        'views/estate_property_offer_view_form.xml',

    ],
}