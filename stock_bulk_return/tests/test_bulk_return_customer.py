# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.tests import Form

from odoo.addons.stock_bulk_return.tests.common import TestStockBulkReturnCommon


class TestBulkReturnSale(TestStockBulkReturnCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sale_order_1 = cls.env['sale.order'].create({
            'partner_id': cls.customer.id
        })
        cls.sale_order_2 = cls.env['sale.order'].create({
            'partner_id': cls.customer.id
        })

        cls.line_1_notrack = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order_1.id,
            'product_id': cls.product_notrack.id,
            'product_uom_qty': 5.0,
        })
        cls.line_1_qty = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order_1.id,
            'product_id': cls.product_qty.id,
            'product_uom_qty': 5.0,
        })
        cls.line_2_lot = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order_2.id,
            'product_id': cls.product_lot.id,
            'product_uom_qty': 10.0,
        })
        cls.line_2_serial = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order_2.id,
            'product_id': cls.product_serial.id,
            'product_uom_qty': 2.0,
        })

        cls.sale_order_1.action_confirm()
        cls.sale_order_2.action_confirm()

        picking_type_out = cls.env.ref('stock.picking_type_out').sudo()
        cls.delivery_picking_1 = cls.env['stock.picking'].create({
            'partner_id': cls.customer.id,
            'picking_type_id': picking_type_out.id,
            'state': 'draft',
            'location_id': picking_type_out.default_location_src_id.id,
            'location_dest_id': cls.customer.property_stock_customer.id or cls.env.ref('stock.stock_location_customers').id or picking_type_out.default_location_dest_id.id,
            'sale_id': cls.sale_order_1.id,
        })
        cls.delivery_picking_2 = cls.env['stock.picking'].create({
            'partner_id': cls.customer.id,
            'picking_type_id': picking_type_out.id,
            'state': 'draft',
            'location_id': picking_type_out.default_location_src_id.id,
            'location_dest_id': cls.customer.property_stock_customer.id or cls.env.ref('stock.stock_location_customers').id or picking_type_out.default_location_dest_id.id,
            'sale_id': cls.sale_order_2.id,
        })

        cls.stock_move_1_notrack = cls.env['stock.move'].create({
            'name': cls.delivery_picking_1.name,
            'picking_id': cls.delivery_picking_1.id,
            'product_id': cls.product_notrack.id,
            'product_uom_qty': 5,
            'location_id': cls.delivery_picking_1.location_id.id,
            'location_dest_id': cls.delivery_picking_1.location_dest_id.id,
            'sale_line_id': cls.line_1_notrack.id,
        })
        cls.stock_move_2_qty = cls.env['stock.move'].create({
            'name': cls.delivery_picking_1.name,
            'picking_id': cls.delivery_picking_1.id,
            'product_id': cls.product_qty.id,
            'product_uom_qty': 3,
            'location_id': cls.delivery_picking_1.location_id.id,
            'location_dest_id': cls.delivery_picking_1.location_dest_id.id,
            'sale_line_id': cls.line_1_qty.id,
        })
        cls.stock_move_3_lot = cls.env['stock.move'].create({
            'name': cls.delivery_picking_2.name,
            'picking_id': cls.delivery_picking_2.id,
            'product_id': cls.product_lot.id,
            'product_uom_qty': 10,
            'location_id': cls.delivery_picking_2.location_id.id,
            'location_dest_id': cls.delivery_picking_2.location_dest_id.id,
            'sale_line_id': cls.line_2_lot.id,
            'move_line_ids': [Command.create({
                'picking_id': cls.delivery_picking_2.id,
                'product_id': cls.product_lot.id,
                'lot_id': cls.lot_1.id,
                'quantity': 5,
            })]
        })

        cls.delivery_picking_1.button_validate()
        cls.delivery_picking_2.button_validate()

        cls.sale_order_1._create_invoices()
        cls.sale_order_2._create_invoices()

    def test_bulk_return_from_delivery_barcode(self):
        bulk_return = self.env['stock.bulk.return'].create({
            'partner_id': self.customer.id,
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
        })
        with Form(bulk_return) as wizard:
            wizard._barcode_scanned = self.delivery_picking_1.name
        self.assertEqual(len(wizard.bulk_return_line_ids), 2, "Two bulk return line should be created")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].product_id.id, self.product_notrack.id, "Product should match")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].max_return_qty, 5, "Maximum return quantity should match")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].picking_id, self.delivery_picking_1, "Delivery should match")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].move_id, self.stock_move_1_notrack, "Stock move should match")

        bulk_return.bulk_return_line_ids.update({
            'return_qty': 2,
        })

        bulk_return._action_confirm()
        bulk_return_picking = self.env['stock.picking'].search([], limit=1, order='id desc')
        self.assertEqual(bulk_return_picking.state, 'assigned', "Picking state should be assigned")
        self.assertEqual(bulk_return_picking.picking_type_id, self.env.ref('stock.picking_type_in'), "Picking type should match")
        self.assertEqual(bulk_return_picking.partner_id, self.customer, "Customer should match")
        self.assertEqual(bulk_return_picking.location_id, bulk_return.location_src_id, "Source location should match")
        self.assertEqual(bulk_return_picking.location_dest_id, bulk_return.location_dest_id, "Destination location should match")

        self.assertEqual(len(bulk_return_picking.move_ids_without_package), 2, "Two stock moves should be created")
        self.assertEqual(bulk_return_picking.move_ids_without_package[0].product_id, self.product_notrack, "Product should match")
        self.assertEqual(bulk_return_picking.move_ids_without_package[0].product_uom_qty, 2, "Return quantity should match")
        self.assertEqual(bulk_return_picking.move_ids_without_package[1].product_id, self.product_qty, "Product should match")
        self.assertEqual(bulk_return_picking.move_ids_without_package[1].product_uom_qty, 2, "Return quantity should match")

        bulk_return_picking.button_validate()
        bulk_return_picking.action_create_credit_note()
        self.assertEqual(bulk_return_picking.credit_note_id.state, 'draft', "Credit note state should be draft")
        self.assertEqual(bulk_return_picking.credit_note_id.move_type, 'out_refund', "Credit note type should be out_refund")
        self.assertEqual(bulk_return_picking.credit_note_id.partner_id, self.customer, "Customer should match")

        self.assertEqual(len(bulk_return_picking.credit_note_id.invoice_line_ids), 2, "Two invoice lines should be created")
        self.assertEqual(bulk_return_picking.credit_note_id.invoice_line_ids[0].product_id, self.product_notrack, "Product should match")
        self.assertEqual(bulk_return_picking.credit_note_id.invoice_line_ids[0].quantity, 2, "Return quantity should match")
        self.assertEqual(bulk_return_picking.credit_note_id.invoice_line_ids[1].product_id, self.product_qty, "Product should match")
        self.assertEqual(bulk_return_picking.credit_note_id.invoice_line_ids[1].quantity, 2, "Return quantity should match")

    def test_bulk_return_from_product_barcode(self):
        bulk_return = self.env['stock.bulk.return'].create({
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'partner_id': self.customer.id,
        })

        with Form(bulk_return) as wizard:
            wizard._barcode_scanned = self.product_notrack.barcode
        self.assertEqual(len(wizard.bulk_return_line_ids), 1, "Atleast one bulk return line should be created")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].product_id.id, self.product_notrack.id, "Product should match")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].max_return_qty, 5, "Maximum return quantity should match")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].picking_id, self.delivery_picking_1, "Delivery should match")
        self.assertEqual(bulk_return.bulk_return_line_ids[0].move_id, self.stock_move_1_notrack, "Stock move should match")

        bulk_return.bulk_return_line_ids.update({
            'return_qty': 2,
        })
        bulk_return._action_confirm()

        bulk_return_picking = self.env['stock.picking'].search([], limit=1, order='id desc')
        self.assertEqual(bulk_return_picking.picking_type_id, self.env.ref('stock.picking_type_in'), "Picking type should match")
        self.assertEqual(bulk_return_picking.partner_id, self.customer, "Customer should match")
        self.assertEqual(bulk_return_picking.state, 'assigned', "Picking state should be assigned")
        self.assertEqual(bulk_return_picking.move_ids.product_id, self.product_notrack, "Product should match")
        self.assertEqual(bulk_return_picking.move_ids.product_uom_qty, 2, "Product quantity should match")
        self.assertEqual(bulk_return_picking.move_ids.location_id, self.env.ref('stock.stock_location_customers'), "Location should match")
        self.assertEqual(bulk_return_picking.move_ids.location_dest_id, self.env.ref('stock.stock_location_stock'), "Location should match")
        self.assertEqual(bulk_return_picking.move_ids.state, 'waiting', "Stock move state should be draft")

        bulk_return_picking.button_validate()
        bulk_return_picking.action_create_credit_note()

        self.assertEqual(bulk_return_picking.credit_note_id.state, 'draft', "Credit note state should be draft")
        self.assertEqual(bulk_return_picking.credit_note_id.move_type, 'out_refund', "Credit note type should be out_refund")
        self.assertEqual(bulk_return_picking.credit_note_id.partner_id, self.customer, "Customer should match")

        self.assertEqual(len(bulk_return_picking.credit_note_id.invoice_line_ids), 1, "Two invoice lines should be created")
        self.assertEqual(bulk_return_picking.credit_note_id.invoice_line_ids[0].product_id, self.product_notrack, "Product should match")
        self.assertEqual(bulk_return_picking.credit_note_id.invoice_line_ids[0].quantity, 2, "Return quantity should match")
