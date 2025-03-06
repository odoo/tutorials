{
    'name': 'Extended Description',
    'version': '0.1',
    'summary': 'this will allow user to add detailed and formatted description for product',
    'description': """
Introduces a new HTML extended description field for products, supporting rich text formatting such as bullet points and lists.
Allows users to add multilingual descriptions for products.
Enables import/export functionality for the extended description.
    """,
    'author': 'odoo',
    'depends': ['website_sale'],
    'data': [
        'views/product_views.xml',
        'views/product_templates.xml'
    ],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
