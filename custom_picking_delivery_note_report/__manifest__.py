{
    'name': 'MO delivery note(Inventory)',
    'description': "Module used to add MO delivery note report in stock(inventory) module",
    'installable': True,
    'application': False,
    'depends': ['stock'],
    'data': [
        'report/mo_report_deliveryslip_template.xml',
        'report/custom_picking_delivery_note_report.xml',
    ],
    'license':'LGPL-3'
}
