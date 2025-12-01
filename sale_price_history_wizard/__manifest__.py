{
    "name": 'Sales Price History',
    "summary": "Adds a button to display the last five sales prices of a product for a selected customer.",
    "depends": ['sale_management'],
    "data": [
        'security/ir.model.access.csv',
        'views/sale_price_history_wizard_view.xml',
        'views/view_order_form.xml'
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3"
}
