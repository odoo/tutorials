{
    'name': 'Product Image Popup',
    'version': '1.0',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['base', 'product', 'web'],
    'data': [
        'views/product_catalog_kanban.xml',
  
    ],
    'assets': {
        'web.assets_backend': [
            'Redesign_Catalog_view/static/src/**/*',
            
        ],
        'web.assets_frontend': [
            'Redesign_Catalog_view/static/src/**/*',  
            
        ],
    },

    'installable': True,
    'application': True,
    
}
