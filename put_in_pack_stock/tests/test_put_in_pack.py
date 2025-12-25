from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestPutInPack(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestPutInPack, cls).setUpClass()

        #Create a Test Product 
        cls.productDenim = cls.env['product.product'].create({
            'name': 'Denim Jeans',
            'type': 'consu',
            'tracking': 'none'
        })

        cls.productKurti = cls.env['product.product'].create({
            'name': 'Kurti',
            'type': 'consu',
            'tracking': 'lot'
        })

        # Create a Test Picking Type with 'Put In Pack' enabled
        cls.picking_type = cls.env['stock.picking.type'].create({
            'name': 'Test Picking Type',
            'sequence_code': 'outgoing',
            'put_in_pack_toggle': True
        })

        # Create a Test Picking
        cls.picking = cls.env['stock.picking'].create({
            'picking_type_id': cls.picking_type.id,
            'put_in_pack_toggle': True
        })

        # Create a Test Stock Move
        cls.move_productDenim = cls.env['stock.move'].create({
            'name': 'Denim Move',
            'product_id': cls.productDenim.id,
            'product_uom_qty': 10,
            'product_uom': cls.env.ref('uom.product_uom_unit').id,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'location_dest_id': cls.env.ref('stock.stock_location_customers').id,
            'picking_id': cls.picking.id,
            'picking_type_id': cls.picking.picking_type_id.id,
        })
        cls.move_productKurti = cls.env['stock.move'].create({
            'name': 'Kurti Move',
            'product_id': cls.productKurti.id,
            'product_uom_qty': 10,
            'product_uom': cls.env.ref('uom.product_uom_unit').id,
            'location_id': cls.env.ref('stock.stock_location_stock').id,
            'location_dest_id': cls.env.ref('stock.stock_location_customers').id,
            'picking_id': cls.picking.id,
            'picking_type_id': cls.picking_type.id,
            'has_tracking': 'lot'
        })

    def test_action_custom_put_in_pack_productDenim(self):
        """Test the custom put in pack action for Denim Jeans"""
        self.move_productDenim.action_custom_put_in_pack()
        self.assertTrue(self.move_productDenim.move_line_ids.result_package_id, "Denim Jeans Package was not created correctly")

    def test_action_custom_put_in_pack_productKurti(self):
        """Test the custom put in pack action for Kurti"""
        self.move_productKurti.action_custom_put_in_pack()
        self.assertTrue(self.move_productKurti.move_line_ids.result_package_id, "Kurti Package was not created correctly")

    def test_no_quantity_to_pack(self):
        """Ensure error is raised when no quantity is available to package"""
        self.move_productDenim.product_uom_qty=0
        with self.assertRaises(UserError):
            self.move_productDenim.action_custom_put_in_pack()
    
    def test_package_size_handling(self):
        """Ensure package size is correctly handled when generating packages."""
        self.move_productDenim.package_size = 4
        self.move_productDenim.package_qty = 3
        self.move_productDenim.action_generate_package()

        self.assertEqual(len(self.move_productDenim.move_line_ids), 3, "Package size handling incorrect.")

    def test_multiple_packages_for_lots(self):
        """Ensure that products tracked by lots generate multiple packages correctly."""
        lot = self.env['stock.lot'].create({
            'name': 'KURTI-001',
            'product_id': self.productKurti.id,
        })
        move_line = self.env['stock.move.line'].create({
            'move_id': self.move_productKurti.id,
            'product_id': self.productKurti.id,
            'qty_done': 10,
            'lot_id': lot.id
        })
        self.move_productKurti.package_size = 2
        self.move_productKurti.action_generate_package()
        self.assertTrue(self.move_productKurti.move_line_ids.result_package_id, "Lot-based packaging not created.")
