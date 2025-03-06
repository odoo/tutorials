# -*- coding: utf-8 -*-
{
    'name': "Add Zero Quantity",
    'description': """
        Adding the zero quantity on account move line.
        If it is checked the quantity would be passed as 0 in einvoicing
    """,
    'author': "Odoo S.A.",
    'category': 'Tutorials/AddZeroQuantity',
    'installable': True,
    'depends': ['l10n_in_edi'],
    'data': [
        'views/view_move_line_form.xml',
    ],
    'license': 'AGPL-3'
}
