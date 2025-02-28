{
    'name' : "Import/Modify Products",
    'version' : "1.0",
    'depends' : [
        'sale',
        'sale_management'
    ],
    'category' : 'Sales/Sales',
    'auther' : "Soham Zadafiya [soza]",
    'description' : """
        Vender can import or modify multiple product by excel file
    """,
    'application' : True,
    'data' : [
        'security/ir.model.access.csv',
        'views/vendor_template_formate_view.xml',
        'views/vendor_product_template_view.xml',
        'views/vendor_product_import_view.xml',
        'views/menus.xml',
        'views/product_template_view.xml',
        'data/ir_sequence_data.xml'
    ],
    'license' : 'LGPL-3'
}