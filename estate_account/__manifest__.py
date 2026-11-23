{
    "name": "Estate Accounting",
    "summary": "Integrate Estate with Accounting",
    "description": """
    Integrates the Estate application with Accounting to automatically generate
    customer invoices when properties are sold, include selling commissions and
    administrative fees, and provide direct access to generated invoices from
    properties.
    """,
    "version": "1.0",
    "depends": ["estate", "account"],
    "data": ['views/estate_property.xml'],
    "auto_install": True,
    "author": "Smit Patel",
    "application": False,
    "installable": True,
    "license": "LGPL-3",
}
