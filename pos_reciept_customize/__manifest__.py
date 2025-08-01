{
    "name": "POS Receipt Customization",
    "summary": "Customizable POS receipt with layouts and HTML header/footer",
    "depends": ["point_of_sale"],
    "category": "Point of Sale",
    "author": "Rohit",
    "installable": True,
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "wizard/reciepts_layout_view.xml",
    ],
}
