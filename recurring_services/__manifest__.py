{
    "name": "Recurring Service",
    "version": "1.0",
    "summary": "Allow adding recurring service product tasks in projects.",
    "description": """
        This module enables the creation of recurring tasks based on the next scheduled service date until the subscription end date.
    """,
    "depends": ["sale_subscription","hr_holidays","sale_project"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    'license': 'LGPL-3'
}
