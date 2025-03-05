{
    "name": "POS Salesperson Selection",
    "version": "1.0",
    "author": "Krishna Patel",
    "depends": ["point_of_sale", "hr"],
    "data": [
        "views/pos_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "sale_person_in_pos/static/src/**/*",
        ],
    },
    "installable": True,
    "license": 'LGPL-3',
}
