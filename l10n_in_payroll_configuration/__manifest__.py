{
    'name': 'Indian Payroll Configuration',
    'author': "Kartavya Desai (kade)",
    'category': 'Human Resources/Payroll',
    'depends': [
        'l10n_in_hr_payroll',
    ],
    'description': """
        Adds features to Indian localization for HR Payroll in Odoo
        - essential salary components and tax-related fields
        - allows setting defaults from payroll configuration
    """,
    'data': [
        'data/ir_default_data.xml',
        'views/res_config_settings_views.xml',
        'views/hr_contract_views.xml',
    ],
    'demo': [
        'data/l10n_in_payroll_config_contract_demo.xml',
    ],
    'license': 'OEEL-1',
}
