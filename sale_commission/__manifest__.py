{
    'name': 'Sale Commission',
    'version': '1.0',
    'category': 'Sales/Commission',
    'summary': "Manage your salespersons' commissions",
    'depends': ['sale_management'],
    'data': [
        'demo/commission_rule.xml',
        'views/commission_rule_views.xml',
        'report/commission_report.xml',
        'views/commission_menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
