{
    'name': 'pricelist_price',
    'version': '1.0',
    'category': 'sale_order/invoice',
    'depends': ['sale_management','account'],
    'sequence' : 1 ,
    'description' :""" This is the pricelist_price module to 
    diplay the book price on the sales order and customer invoices """,
    'license':'LGPL-3' ,
    'installable':'True' ,
    'data': [
        "views/sales_order_views.xml",
        "views/account_move_views.xml",
    ],
    "application": True,
}
