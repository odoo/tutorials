{
    'name': 'MRP - Modular Types',
    'version': '1.0',
    'summary': 'Modular Types in MRP for BOM',
    'author': 'Harsh Shah',
    'license': 'LGPL-3',
    'installable': True,
    'depends': [ 'sale_mrp', 'sale_management' ],
    'data': [
        'security/ir.model.access.csv',

        'views/product_template_view.xml',
        'views/mrp_bom_view.xml',
        'views/sale_mrp_modular_wizard_view.xml',
        'views/sale_order_view.xml',
        'views/mrp_production_view.xml'
    ],
}

