from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('post_install', '-at_install')
class TestMultiWarehouseAllocation(TransactionCase):

    def setUp(self):
        """Set up test environment"""
        super().setUp()

        self.product_model = self.env['product.product']
        self.stock_quant = self.env['stock.quant']
        self.sale_order_model = self.env['sale.order']
        self.sale_order_line_model = self.env['sale.order.line']
        self.stock_picking_model = self.env['stock.picking']
        self.warehouse_model = self.env['stock.warehouse']

        self.primary_warehouse = self.warehouse_model.create({'name': 'Primary Warehouse', 'code': 'PRI'})
        self.secondary_warehouse = self.warehouse_model.create({'name': 'Secondary Warehouse', 'code': 'SEC'})

        self.product = self.product_model.create({
            'name': 'Test Product',
            'is_storable': True,
            'primary_warehouse_id': self.primary_warehouse.id,
            'secondary_warehouse_id': self.secondary_warehouse.id,
        })

        self.product_2 = self.product_model.create({
            'name': 'Test Product 2',
            'is_storable': True,
            'primary_warehouse_id': self.primary_warehouse.id,
            'secondary_warehouse_id': self.secondary_warehouse.id
        })

    def test_create_product_without_warehouse(self):
        """Test creating a product without assigning a warehouse."""
        product_without_warehouse = self.product_model.create({
            'name': 'Product Without Primary Warehouse',
            'is_storable': True,
        })
        self.assertEqual(product_without_warehouse.primary_warehouse_id.id, False, "Product should have a primary warehouse.")

    def test_delivery_order_creation_single_warehouse(self):
        """Test that a single delivery order is created when stock is available in one warehouse."""
        self.stock_quant.create({
            'product_id': self.product.id,
            'location_id': self.primary_warehouse.lot_stock_id.id,
            'quantity': 10,
        })

        self.stock_quant.create({
            'product_id': self.product_2.id,
            'location_id': self.primary_warehouse.lot_stock_id.id,
            'quantity': 10,
        })

        order = self.sale_order_model.create({'partner_id': self.env.ref('base.res_partner_1').id})

        self.sale_order_line_model.create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_uom_qty': 5,
            'warehouse_id': self.primary_warehouse.id,
        })

        self.sale_order_line_model.create({
            'order_id': order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 5,
            'warehouse_id': self.primary_warehouse.id,
        })

        order.action_confirm()
        pickings = self.stock_picking_model.search([('origin', '=', order.name)])
        self.assertEqual(len(pickings), 1, "A single delivery order should be created.")
        self.assertEqual(pickings.location_id, self.primary_warehouse.lot_stock_id, "Delivery order should be from Primary Warehouse.")

    def test_delivery_order_creation_multiple_warehouses(self):
        """Test that multiple delivery orders are created if stock is split across warehouses."""
        self.stock_quant.create({
            'product_id': self.product.id,
            'location_id': self.primary_warehouse.lot_stock_id.id,
            'quantity': 3,
        })

        self.stock_quant.create({
            'product_id': self.product_2.id,
            'location_id': self.secondary_warehouse.lot_stock_id.id,
            'quantity': 5,
        })

        order = self.sale_order_model.create({'partner_id': self.env.ref('base.res_partner_1').id})

        self.sale_order_line_model.create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_uom_qty': 3,
            'warehouse_id': self.primary_warehouse.id,
        })

        self.sale_order_line_model.create({
            'order_id': order.id,
            'product_id': self.product_2.id,
            'product_uom_qty': 5,
            'warehouse_id': self.secondary_warehouse.id,
        })

        order.action_confirm()
        pickings = self.stock_picking_model.search([('origin', '=', order.name)])
        self.assertEqual(len(pickings), 2, "Two delivery orders should be created.")
