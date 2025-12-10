from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.fields import Command
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class RentalDepositTestCase(TransactionCase):
    def setUp(self):
        super().setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })

        self.deposit_product = self.env['product.product'].create({
            'name': 'Deposit Product',
            'rent_ok': True
        })

        self.rental_product = self.env['product.product'].create({
            'name': 'Music System',
            'type': 'consu',
            'require_deposit': True,
            'deposit_amount': 100.0
        })

        self.sale_order = self.env['sale.order'].create({'partner_id': self.partner.id})

    def test_configure_deposit_product(self):

        with self.assertRaises(UserError, msg="Should raise error if deposit product is not configured"):
            self.sale_order.write({
                "order_line": [
                    Command.create({'product_id': self.rental_product.id, 'product_uom_qty': 2}),
                ]
            })

    def test_deposit_line(self):

        self.env['ir.config_parameter'].sudo().set_param('deposit_in_rental_app.deposit_product_id', self.deposit_product.id)

        self.sale_order.write({
            "order_line": [
                Command.create({'product_id': self.rental_product.id, 'product_uom_qty': 2}),
            ]
        })

        main_line = self.sale_order.order_line.filtered(lambda l: not l.is_deposit_line)
        deposit_line = self.sale_order.order_line.filtered(lambda l: l.is_deposit_line)

        # Check deposit line is created or not
        self.assertTrue(deposit_line, "Deposit line was not created.")

        # Check deposit line is correctly linked
        self.assertIn(deposit_line[0], main_line.child_ids, "Deposit line is not in child_ids of main line.")
        self.assertEqual(deposit_line[0].parent_id, main_line[0], "Deposit line's parent_id does not point to the main line.")

        main_line.write({'product_uom_qty': 5})

        # Check deposit line quantity is also updated
        self.assertEqual(
            deposit_line.product_uom_qty, 5,
            "Deposit line quantity should update when main line quantity changes"
        )
