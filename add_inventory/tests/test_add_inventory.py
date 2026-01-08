from odoo.tests import tagged
import base64
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestAddInventory(TransactionCase):

    def setUp(self):
        """Set up test environment"""
        super().setUp()
        
        self.wizard_model = self.env['inventory.import.wizard']
        self.product_model = self.env['product.product']
        self.stock_quant = self.env['stock.quant']
        self.stock_picking = self.env['stock.picking']
        self.stock_lot = self.env['stock.lot']
        self.location = self.env.ref('stock.stock_location_stock')
        self.picking_type_in = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        self.picking_type_out = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
    
    def test_error_if_file_not_csv(self):
        """Test that an error is raised if the uploaded file is not a CSV"""

        file_content = "This is a test file and not a CSV."
        file_encoded = base64.b64encode(file_content.encode('utf-8'))

        wizard = self.wizard_model.create({
            'file': file_encoded,
            'file_name': 'test.txt',
            'location_id': self.location.id,
            'operation': 'add',
        })

        with self.assertRaises(ValidationError):
            wizard.action_import()
    

    def test_add_inventory_without_serial_or_lot(self):
        """Test adding inventory where no serial number or lot is provided"""

        file_content = "Product Name,Serial Number,Quantity,UOM,HSN Code\nTest Product Without Lot,,10,Unit,1234"
        file_encoded = base64.b64encode(file_content.encode('utf-8'))

        wizard = self.wizard_model.create({
            'file': file_encoded,
            'file_name': 'test_inventory.csv',
            'location_id': self.location.id,
            'operation': 'add',
        })

        wizard.action_import()

        product = self.product_model.search([('name', '=', 'Test Product Without Lot')], limit=1)
        self.assertTrue(product, "Product should be created.")

        stock_quant = self.stock_quant.search([
            ('product_id', '=', product.id),
            ('location_id', '=', self.location.id)
        ], limit=1)
        self.assertTrue(stock_quant, "Stock quant should be created.")
        self.assertEqual(stock_quant.quantity, 10, "Stock quantity should be updated correctly.")

        stock_lot = self.stock_lot.search([('product_id', '=', product.id)], limit=1)
        self.assertFalse(stock_lot, "Lot should not be created since no serial number was provided.")
    
    def test_add_inventory_with_serial_or_lot(self):
        """Test that inventory adjustment and lot are created if serial number is provided"""

        file_content = "Product Name,Serial Number,Quantity,UOM,HSN Code\nTest Product With Lot,SN001,5,Unit,1234"
        file_encoded = base64.b64encode(file_content.encode('utf-8'))

        wizard = self.wizard_model.create({
            'file': file_encoded,
            'file_name': 'test_inventory.csv',
            'location_id': self.location.id,
            'operation': 'add',
        })

        wizard.action_import()

        product = self.product_model.search([('name', '=', 'Test Product With Lot')], limit=1)
        self.assertTrue(product, "Product should be created.")

        stock_lot = self.stock_lot.search([
            ('name', '=', 'SN001'),
            ('product_id', '=', product.id)
        ], limit=1)
        self.assertTrue(stock_lot, "Lot should be created.")

        stock_quant = self.stock_quant.search([
            ('product_id', '=', product.id),
            ('location_id', '=', self.location.id),
            ('lot_id', '=', stock_lot.id)
        ], limit=1)
        self.assertTrue(stock_quant, "Stock quant should be created for lot-tracked product.")

        inventory = self.stock_inventory.search([], limit=1)
        self.assertTrue(inventory, "Inventory adjustment should be created for lot-tracked product.")
    
    def test_remove_inventory_with_and_without_lot(self):
        '''Test removing inventory with and without a lot/serial number when stock is insufficient'''

        product = self.product_model.create({
            'name': 'Test Product',
            'is_storable': True,
            'type': 'product',
            'tracking': 'lot', 
            'uom_id': self.env.ref('uom.product_uom_unit').id,
        })

        lot = self.stock_lot.create({
            'name': 'TEST-LOT-001',
            'product_id': product.id,
        })

        self.stock_quant.create({
            'product_id': product.id,
            'location_id': self.location.id,
            'quantity': 3, 
        })

        self.stock_quant.create({
            'product_id': product.id,
            'location_id': self.location.id,
            'quantity': 2,  
            'lot_id': lot.id, 
        })

        file_content = """Product Name,Serial Number,Quantity,UOM,HSN Code
                         Test Product,,5,m,1234
                         Test Products,TEST-LOT-001,5,lb,1234"""
        file_encoded = base64.b64encode(file_content.encode('utf-8'))

        wizard = self.wizard_model.create({
            'file': file_encoded,
            'file_name': 'test_remove_inventory.csv',
            'location_id': self.location.id,
            'operation': 'remove',
        })

        wizard.action_import()

        stock_quant_no_lot = self.stock_quant.search([
            ('product_id', '=', product.id),
            ('location_id', '=', self.location.id),
            ('lot_id', '=', False)
        ], limit=1)
        
        stock_quant_with_lot = self.stock_quant.search([
            ('product_id', '=', product.id),
            ('location_id', '=', self.location.id),
            ('lot_id', '=', lot.id)
        ], limit=1)

        self.assertEqual(stock_quant_no_lot.quantity, 3, "Stock quantity should remain unchanged for untracked product if removal is not possible.")
        self.assertEqual(stock_quant_with_lot.quantity, 2, "Stock quantity should remain unchanged for lot-tracked product if removal is not possible.")
