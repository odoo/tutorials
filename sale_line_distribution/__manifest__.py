{
    'name': "Sale Line Distribution",
    'version': "1.0",
    'author': "Vaidik Gorasiya - vrgo",
    'depends': ['base', 'sale_management'],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_line_distribution_wizard.xml",
        "views/sale_order_view.xml"
    ],
    'installable': True,
    'license': 'LGPL-3',
}
