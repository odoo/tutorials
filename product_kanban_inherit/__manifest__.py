{
    "name": "Product Kanban Inherit",
    "version": "1.0",
    "summary": "Customize Product Kanban View for Mobile",
    "description": "This module enlarges the product image in the kanban view for mobile screens.",
    "author": "Krishna Patel",
    "category": "Customization",
    "depends": ["product","sale_management"],
    "data": [
        "views/product_kanban_inherit.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_kanban_inherit/static/src/scss/product_kanban.scss",
            "product_kanban_inherit/static/src/js/extended_template.xml",
            "product_kanban_inherit/static/src/js/extended_image.js",
        ],
    },
    "installable": True,
    "auto_install": True,
    "license": "LGPL-3",
}
