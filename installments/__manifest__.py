{
    'name': 'installments',
    'version': '1.0',
    'author' : 'Dhruv Chauhan',
    'icon': '/installments/static/description/icon.png',
    'description': 'Enables sales order payments via EMIs.',
    'summary': 'Adds EMI payment functionality, penalty management, and required document upload to the Sales module.',
    'depends': ['sale_management', 'documents'],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_cron.xml',
        'data/product_data.xml',
        'data/document_document_demo.xml',

        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        
        'wizard/installment_wizard.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3', 
}
