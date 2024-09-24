{
    "name": "installment",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "sale_subscription", "documents"],
    "description": "Installment Application",
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/installment_setting_view.xml",
        "wizard/add_emi_view.xml",
        "views/installment_menu.xml",
        "views/sales_order_view.xml",
        "data/product_data.xml",
        "data/corn.xml",
    ],
}
