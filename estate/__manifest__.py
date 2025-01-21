{
    'name': 'estate',
    'installable': True, #Whether a user should be able to install the module from the Web UI or not.
    'application': True, #Whether the module should be considered as a fully-fledged application (True) or is just a technical module (False) that provides some extra functionality to an existing application module.
    'depends': ['base','web','website'], # any module necessary for this one to work correctly
    'category': 'Real Estate/Brokerage', # category(module_category)/subcategory
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv', #security access
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_views.xml',#actions defs & views to be shown
        'views/estate_menus.xml', #estate root-menu, first level menu, action menu to be shown/ above because id refers to estate_property_views' id
        'views/estate_property_res_user_view_form.xml',
        'wizard/estate_property_make_offer_wizard_view.xml',
        'views/estate_property_multi_view_web_page.xml',
        'views/estate_property_single_view_web_page.xml'
    ],
    'demo': [
        'demo/estate.property.type.csv',
        'demo/estate_property.xml',
        'demo/estate_property_offer.xml'
    ],
    'license':'LGPL-3'
} # type: ignore
