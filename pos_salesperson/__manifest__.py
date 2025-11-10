{
    'name':"Salesperson Pos",
    'version':"1.0",
    'author':"sujal_asodariya",
    'Summary':"Add salesperson button in pos order to track the salesperson id",
    'description':" In point of sale once they open any session in the shop,In the billing screen. Need to have the salesperson drop-down which has data of all the employees.",
    'depends':["point_of_sale", "hr"],
    'data':[
        "views/pos_order_view.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_salesperson/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
