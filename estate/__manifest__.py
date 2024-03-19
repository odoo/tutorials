{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Tutorials/Estate',
    'summary': 'Real Estate Advertisement',
    'author': 'Muhamed Abdalla (muab)',
    'description':
    """
    The top area of the form view summarizes important information for the property, such as the name, the property type, the postcode and so on.
    The first tab contains information describing the property: bedrooms, living area, garage, garden…
    The second tab lists the offers for the property. We can see here that potential buyers can make offers above or below the expected selling price.
    It is up to the seller to accept an offer.
    """,
    'website': "https://www.odoo.com",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',
        'views/estate_property_menu.xml'
    ],
    'application': True,
    'license': 'AGPL-3'
}
