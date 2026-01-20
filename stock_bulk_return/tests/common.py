# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.tests import TransactionCase


class TestStockBulkReturnCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.customer = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.vendor = cls.env['res.partner'].create({'name': 'Test Vendor'})

        cls.product_notrack = cls.env['product.product'].create({
            'name': 'Product (no tracking)',
            'barcode': '111',
        })
        cls.product_qty = cls.env['product.product'].create({
            'name': 'Product (quantity)',
            'is_storable': True,
            'tracking': 'none',
            'barcode': '222',
        })
        cls.product_lot = cls.env['product.product'].create({
            'name': 'Product (lot)',
            'is_storable': True,
            'tracking': 'lot',
            'barcode': '333',
        })
        cls.product_serial = cls.env['product.product'].create({
            'name': 'Product (serial)',
            'is_storable': True,
            'tracking': 'serial',
            'barcode': '444',
        })

        cls.env['stock.quant'].create({
            'product_id': cls.product_qty.id,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'quantity': 100,
        })

        cls.lot_1 = cls.env['stock.lot'].create({
            'name': 'LOT000100',
            'product_id': cls.product_lot.id,
            'quant_ids': [Command.create({
                'product_id': cls.product_lot.id,
                'location_id': cls.env.ref('stock.stock_location_stock').id,
                'quantity': 5,
            })]
        })
        cls.lot_2 = cls.env['stock.lot'].create({
            'name': 'LOT000200',
            'product_id': cls.product_lot.id,
            'quant_ids': [Command.create({
                'product_id': cls.product_lot.id,
                'location_id': cls.env.ref('stock.stock_location_stock').id,
                'quantity': 5,
            })]
        })
        cls.serial_1 = cls.env['stock.lot'].create({
            'name': 'SRN001',
            'product_id': cls.product_serial.id,
            'quant_ids': [Command.create({
                'product_id': cls.product_serial.id,
                'location_id': cls.env.ref('stock.stock_location_stock').id,
                'quantity': 1,
            })]
        })
        cls.serial_2 = cls.env['stock.lot'].create({
            'name': 'SRN002',
            'product_id': cls.product_serial.id,
            'quant_ids': [Command.create({
                'product_id': cls.product_serial.id,
                'location_id': cls.env.ref('stock.stock_location_stock').id,
                'quantity': 1,
            })]
        })
