{
    'name' : "Add Zero quantity on account move line",
    'version' : "1.0",
    'category' : "Accounting",
    'summary' : "Module to add a boolean field - zero quantity on account move line, if it is checked it will pass product quanity as zero",
    'depends' : ['l10n_in_edi'],
    'data' : [
        'views/account_move_line_views.xml',
    ],
    'installable' : True,
    'license': "AGPL-3",
}
