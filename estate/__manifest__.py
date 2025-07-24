{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Jay Chauhan",
    'category': 'Category',
    'description': """
        Real Estate Management Module

        This module allows managing real estate properties with detailed information including:
        - Property title, description, and postcode
        - Availability date with default scheduling
        - Pricing details (expected and selling price)
        - Property features like bedrooms, living area, facades, garage, and garden
        - Garden specifics including area and orientation
        - Status tracking through different stages: new, offer received, offer accepted, sold, cancelled
        - Active flag to easily archive or activate properties
        - User-friendly views and search with filters and group-by options for efficient property management
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml' 
    ],
    'installable': True,
    'application': True
}
