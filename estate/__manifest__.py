{
    "name": "Real Estate",
    "version": "1.0",
    "summary": "Real Estate Property Management",
    "description": """
        Tutorial module for managing real estate properties.
    """,
    "author": "Your Name",
    "category": "Tutorial",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
        ],
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}
