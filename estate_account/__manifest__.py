{
    "name": "Real Estate Account",
    "version": "1.0",
    "depends": ["estate","account",],
    "description": """
This is Real estate Account module for Accounting and invoice purpose.
    """,
    "data": [
       "report/estate_property_report_inherit.xml",
    ],
    "assets": {
    'web.assets_backend': [
        'estate/static/src/img/*',
    ],
    },
    "license": "LGPL-3",
}
