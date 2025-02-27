{
    'name': "Supplier Portal",
    'description': """
        This custom module create one supplier portal at where suppliers can log in and upload their invoices, considering PDF and XML files. Once they upload the files and send their invoice, one draft bill automatically generate.
    """,
    'author': "Dhruv Godhani",
    'installable': True,
    'depends': ['account','website'],
    'data': [
        "views/supplier_portal_views.xml",
    ],
    'license': 'LGPL-3',
}
