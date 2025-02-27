{
    'name' : "Add Pricelist Price",
    'version' : '1.0',
    'category': 'Sales/Sales',
    'summary' : 'Module to add pricelist price in Sales Order Lines and Account Move Lines',
    'description': """
        This module adds Book price field in invoice line and sales order line to compare 
        between book price (pricelist) and manually adjusetd price on lines.
    """,
    'depends' : ['sale', 'account'],
    'data' : [
        'views/add_pricelist_price_views.xml'
    ],
    'installable' : True,
    'license': 'AGPL-3',
}
