{
    "name": 'Pricelist Price',
    "version": '1.0',
    "description": 'Enables comparision with original pricelist price',
    "depends":[
        'sale_management',
        'account'
    ],
    "data": [
        'views/sale_order_views.xml',
        'views/account_move_views.xml'
    ],
    "license": 'LGPL-3',
    "installable": True,
    "application": False,
    "auto_install": True
}
