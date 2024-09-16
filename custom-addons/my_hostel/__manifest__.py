{
    'name': "Hostel Management",
    'summary': "Hostel Management With Ease",
    'description': """Efficiently manage the entire residential facility in the school.""",
    'author': "Yura Pylypchuk",
    'website': "https://www.yourwebsite.com",
    'category': 'Uncategorized',
    'version': '17.0.1.0.0',  # if the version doesn't match the module version, odoo will update the module.
    'depends': ['base'],
    'data': [
        # files that contains security groups must be loaded before the file with access rights.
        'security/hostel_security.xml',
        'security/ir.model.access.csv',
        'views/hostel.xml',
        'views/hostel_room.xml',
        'data/data.xml'
    ],

    # 'assets': {
    #     'web.assets_backend': [
    #         'web/static/src/xml/**/*',
    #     ],
    #         },
    # 'demo': ['demo.xml'],
}
