{
    "name": "Real Estate",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_property_menus.xml",
    ],
    "demo": [
        "demo/estate_property_demo.xml",
    ],
    'author': 'Hansil Chapadiya',
    'license': 'LGPL-3'
}
