from odoo.tests.common import TransactionCase


class RentalDepositCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.deposit_product = cls.env['product.product'].create({
            'name': 'Deposit Fee',
            'type': 'service',
        })
        cls.env.company.deposit_product = cls.deposit_product

        cls.rental_product_a = cls.env['product.product'].create({
            'name': 'Test Projector',
            'rent_ok': True,
            'requires_deposit': True,
            'deposit_amount': 50.0,
        })

        cls.rental_product_b = cls.env['product.product'].create({
            'name': 'Test Bike',
            'rent_ok': True,
            'requires_deposit': True,
            'deposit_amount': 30.0,
        })

        cls.rental_product_c = cls.env['product.product'].create({
            'name': 'Test Camera',
            'rent_ok': True,
            'requires_deposit': True,
            'deposit_amount': 20.0,
        })

        cls.rental_no_deposit = cls.env['product.product'].create({
            'name': 'Test Chair',
            'rent_ok': True,
            'requires_deposit': False,
        })

        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})

    def _make_order(self):
        """Creates a fresh sale order each time."""
        return self.env['sale.order'].create({
            'partner_id': self.partner.id,
        })

    def _add_line(self, order, product, qty=1, price=10.0):
        """Helper — adds a single order line and returns it."""
        return self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': product.id,
            'product_uom_qty': qty,
            'price_unit': price,
        })
