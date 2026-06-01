{
    "name": "Stock Custom Picking Report",
    "application": False,
    "installable": True,
    "author": "sngoh",
    "depends": ["mrp", "stock"],
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "report/report_mo_delivery_note.xml",
        "report/stock_report_view.xml",
    ],
}
