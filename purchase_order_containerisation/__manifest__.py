# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Order Containerisation',
    'version': '1.0',
    'depends': ['purchase', 'stock'],
    'description': """
This module enables "Containerisation" of Purchase Orders (POs) in Odoo. Users can select a supplier, view open POs, and containerize selected stock move lines into a new or existing container.
It automates PO lifecycle updates, manages transfer adjustments, and ensures accurate tracking of shipments through different statuses (In Production, Containerised, On Water, Customs, Booked In).
The module enhances logistics efficiency by streamlining goods receipt and stock updates.
""",
    'data': [
        'security/ir.model.access.csv',
        'data/picking_type_data.xml',
        'wizard/purchase_order_containerisation_supplier_view.xml',
        'wizard/purchase_order_create_containerisation_view.xml',
        'wizard/containerisation_location_warning_view.xml',
        'views/stock_picking_view.xml',
        'views/purchase_order_containerisation_menuitem_view.xml',
        'views/stock_move_view.xml',
        'views/purchase_order_containerisation_picking_view.xml',
    ],
    'license': 'LGPL-3'
}
