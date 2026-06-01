{
    'name': 'Zero Accounting Approval',
    'description': 'Adding the zero quantity on account move line and If it is checked the quantity would be passed as 0 in einvoicing',
    'depends': ['l10n_in_edi'],
    'author': 'moahi',
    'data': [
        'views/zero_views.xml',
    ],
    'license': 'LGPL-3'
}
