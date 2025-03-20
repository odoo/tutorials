{
    'name': "Product Category Global Info",
    'version': '1.0',
    'summary': 'Extends product category with global info fields and a new tab grouping attributes by category.',
    'description': """
                This module extends the product category form by:
                - Adding a boolean field "Show on Global Info"
                - Adding a many2many field to map required attributes
                It also adds a new tab called "Global Info" that displays category and attribute information grouped by product category.
                """,
    'category': 'Productivity',
    'depends': ['stock', 'sale_management'],
    'data': [
        'views/product_category_global_info.xml',
        'views/sale_order_view_inherit.xml',
    ],
    'license': 'AGPL-3'
}
