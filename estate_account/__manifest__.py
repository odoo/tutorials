{
    "name": "Estate Account",
    "version": "1.0",
    "sequence": 2,
    "depends": ["estate", "account"],
    "description": """
    This is the link module that helps generating invoices when marking the property as sold.
    """,
    "license": "LGPL-3",

    "data": [
        'views/estate_property_views.xml',
        'reports/estate_property_reports.xml',
    ]
}
