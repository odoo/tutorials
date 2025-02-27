from odoo.tests.common import TransactionCase
from odoo.tests.form import Form
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('-at_install', 'post_install')
class TestRentalDeposit(TransactionCase):
    
    
    @classmethod
    def setUpClass(cls):
        super(TestRentalDeposit, cls).setUpClass()
        
        cls.deposit_product_id = cls.env['product.product'].create({
            'name': 'Security Deposit',
            'type': 'service',
            
        })
        
        cls.env.company.deposit_product_id = cls.deposit_product_id
        
        cls.rental_product = cls.env['product.product'].create({
            'name': 'Rental Car',
            'type': 'consu',
            'requires_deposit' : True,
            'deposit_amount': 100.0,
        })
        
        cls.partner1 = cls.env['res.partner'].create([
            {'name': 'Partner 1'},
        ])
        
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner1.id,
        })
        

    def test_deposit_line_added(cls):
        """
        Ensure that deposit lines are added when ordering a rental product.
        """
        order_line = cls.env['sale.order.line'].create({
            'order_id': cls.sale_order.id,
            'product_id': cls.rental_product.id,
            'product_uom_qty': 1,
            'price_unit': 500.0,
        })

        cls.sale_order._onchange_add_product()

        deposit_line = cls.sale_order.order_line.filtered(
            lambda l: l.product_id == cls.deposit_product_id
        )
        cls.assertTrue(deposit_line, "Deposit line should be added")
        cls.assertEqual(
            1, 
            deposit_line.product_uom_qty, 
            "Deposit quantity should match rental product"
        )
        cls.assertEqual(
            100.0,
            deposit_line.price_unit,
            "Deposit amount should match the rental product's deposit amount"
        )
        
    def test_deposit_line_updates(cls):
        """
        Ensure that deposit lines are updated 
        when rental product quantity updates.
        """
        sale_order_form = Form(cls.sale_order)
        
        with sale_order_form.order_line.new() as line:
            line.product_id = cls.rental_product
            line.product_uom_qty = 2
            line.price_unit = 500.0
            
        sale_order = sale_order_form.save()
        
        deposit_line = sale_order.order_line.filtered(
            lambda l: l.product_id == cls.deposit_product_id
        )
        
        cls.assertEqual(
            deposit_line.product_uom_qty,
            3,
            "Deposit quantity should be be updated."
        )
