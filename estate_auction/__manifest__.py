{
    'name': "Real Estate Auction",
    'version': '1.0',
    'depends': ['base', 'mail', 'website', 'estate'],
    'category': 'Real Estate/Brokerage',
    'author': "Soham Zadafiya [soza]",
    'description': """
        Autometed Auction For Real Estate
    """,
    'application': True,
    'data' : [
        'views/estate_property_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_website_template.xml'
    ],
    'license': 'LGPL-3'
}
