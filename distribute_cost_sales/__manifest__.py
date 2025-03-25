{
    'name': "Distribute Cost - Sales",
    'version': "1.0",
    'category': "Sales/Sales",
    'summary': "Distribute cost over other salesline",
    'depends': [
        'sale'
    ],
    'description': """
        This module divides sale order line price to other sale order lines
    """,
    'data' : [
        'security/ir.model.access.csv',
        'wizard/cost_distribution_wizard.xml',
        'views/sale_order_views.xml',
    ],
    'installable' : True,
    'license': "AGPL-3"
}
