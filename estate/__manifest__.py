{
    'name': "Real Estate",

    'summary': """
        Real Estate management module developed throughout the Odoo Web Framework tutorial
    """,

    'description': """
        This module is developed across the full tutorial series
        "Master the Odoo Web Framework".

        Throughout approximately 15 chapters, the Real Estate application is built
        step by step to demonstrate core Odoo development concepts, including:

        - Module structure and manifest configuration
        - Creating and extending models
        - Field types and computed fields
        - Business logic and constraints
        - Views (form, tree, kanban, search)
        - Actions and menus
        - Security and access rights
        - ORM features and inheritance
        - Server actions and automated actions
        - Customizations and best practices

        The module serves as a complete practical example of how to design,
        develop, and extend a business application using Odoo.
    """,


    'author': "Odoo S.A.",
    'website': "https://www.odoo.com/",
    'category': 'Tutorials',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml'
    ],
    'license': 'AGPL-3'
}
