{
    'name': 'Real Estate XML',
    'license': "GPL-3",
    'depends': [
        'base',
        'base_import_module',
        'website',
    ],
    'data': [
        "models/property_type.xml",
        "models/property_tags.xml",
        "models/property_offer.xml",
        "models/property.xml",
        "views/property_views.xml",
        "security/ir.model.access.csv",
    ],
}
