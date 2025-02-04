{
    "name": "Real Estate",
    "summary": "Real Estate Module helps to buy and sell Properties.",
    "description": "",
    "application": True,
    "category": "Tutorials",
    "installable": True,
    "depends": ['base'],
    "data": [
        'security/ir.model.access.csv', 
        'views/real_estate_property_views.xml', 
        'data/real_estate_property_data.xml', 
        'views/real_estate_menu_views.xml'
    ],
    'license': 'AGPL-3',
}
