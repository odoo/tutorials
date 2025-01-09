{
    'name': 'installments',
    'version': '1.0',
    'author' : 'Dhruv Chauhan',
    'description': 'Enables sales order payments via EMIs.',
    'summary': 'Adds EMI payment functionality, penalty management, and required document upload to the Sales module.',
    'depends': ['base', 'sale_management', 'documents'],
    'data': [
        'security/ir.model.access.csv',

        'data/product_data.xml',
        'data/ir_cron.xml',
        'data/document_document_demo.xml',

        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
        
        'wizard/installment_wizard.xml'
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3', 
}
