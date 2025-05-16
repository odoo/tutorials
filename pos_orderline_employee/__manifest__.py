{
    "name": "POS orderline employee",
    "version": "1.0",
    "summary": "Add employee selection feature in POS order lines",
    "description": """
    This module enhances the Point of Sale (POS) module by introducing an "Select Employee" button in the POS interface.
    - Allows users to assign employees to POS order lines.
    - Each service product can be assigned to a different employee.
    - Employee selection is stored and available in reports for tracking.
    """,
    "depends": ["pos_hr"],
    "data": [
        "views/pos_order_view.xml",
        "views/pos_order_report_view.xml",
        "views/hr_employee_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_orderline_employee/static/src/**/*",
        ],
        "web.assets_tests": [
            "pos_orderline_employee/static/tests/tours/**/*",
        ]
    },
    "auto_install": True,
    "license": "LGPL-3",
}
