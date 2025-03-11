{
    'name' : "POS order workflow",
    'version' : "1.0",
    'depends' : ['point_of_sale'],
    'category' : "Sales/Point of Sale",
    'description' : "A module for handling POS order work flow",
    'installable' : True,
    "assets": {
        'point_of_sale._assets_pos': [
           "pos_order_workflow/static/src/**/*",
        ],
    },
    'license': "AGPL-3"
}
