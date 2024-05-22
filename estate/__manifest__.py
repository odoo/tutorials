{
    "name": "estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "odoo dev",
    "category": "Category",
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "description": """
    Description text
    """,
    # # data files always loaded at installation
    "data": [
        # 'views/mymodule_view.xml',
        "security/ir.model.access.csv"
    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
}
