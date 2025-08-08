{
    "name": "Estate Account",
    "depends": ["estate", "account"],  # This ensures both modules are installed
    "data": [
        'views/estate_property_views.xml',
        'report/estate_report.xml',
    ],
    'license': 'LGPL-3',
    "application": True,
}
