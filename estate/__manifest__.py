{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'installable': True,
    'author': "Demat",
    'license': "AGPL-3",
    'data': [
        "models/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/menu_estate_property.xml",
        "views/list_estate_property.xml",
        "views/form_estate_property.xml",
        "views/search_estate_property.xml"
    ]
}
