{
    'name': 'New Mrp',
    'version': '1.0',
    'description': 'Custom MO Delivery Note report without Kit Products(in Inventory)',
    'depends': ['mrp', 'sale_management'],
    'data': [
        'report/report_mo_delivery_note_views.xml',
        'report/report_mo_delivery_note.xml',
    ],
    'license': 'LGPL-3',
}
