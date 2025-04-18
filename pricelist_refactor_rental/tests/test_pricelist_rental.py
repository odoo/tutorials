from odoo import fields
from dateutil.relativedelta import relativedelta
from odoo.fields import Command
from ...pricelist_refactor_base.tests.test_pricelist_base import TestPricelistBase


class TestPricelistRental(TestPricelistBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.recurrence_hourly = cls.env['sale.temporal.recurrence'].create({
            'duration': 1.0,
            'unit': 'hour'
        })
        cls.recurrence_daily = cls.env['sale.temporal.recurrence'].create({
            'duration': 1.0,
            'unit': 'day'
        })

        cls.test_rent = cls.env['product.product'].create({
            'name': 'Projector',
            'rent_ok': True,
            'extra_hourly': 7.0,
            'extra_daily': 30.0,
        })
        cls.test_rent_template_id = cls.test_rent.product_tmpl_id

        cls.pricelist_id1 = cls.env['product.pricelist'].create({
            'name': 'Rental Pricelist 1',
            'product_rental_pricelist_ids': [
                Command.create({
                    'compute_price': 'fixed',
                    'recurrence_id': cls.recurrence_hourly.id,
                    'fixed_price': 10,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product',
                }),
                Command.create({
                    'compute_price': 'fixed',
                    'recurrence_id': cls.recurrence_hourly.id,
                    'fixed_price': 5,
                    'min_quantity': 2,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product',
                }),
                Command.create({
                    'compute_price': 'fixed',
                    'recurrence_id': cls.recurrence_daily.id,
                    'fixed_price': 100,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product',
                }),
            ]
        })

        cls.pricelist_id2 = cls.env['product.pricelist'].create({
            'name': 'Rental Pricelist 2',
            'product_rental_pricelist_ids': [
                Command.create({
                    'compute_price': 'percentage',
                    'recurrence_id': cls.recurrence_hourly.id,
                    'percent_price': 10,
                    'base': 'pricelist',
                    'base_pricelist_id': cls.pricelist_id1.id,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product',
                }),
                Command.create({
                    'compute_price': 'formula',
                    'recurrence_id': cls.recurrence_daily.id,
                    'base': 'pricelist',
                    'base_pricelist_id': cls.pricelist_id1.id,
                    'price_surcharge': -10,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product',
                }),
            ]
        })

        cls.rent_order = cls.env['sale.order'].create({
            'name': 'Test Rental',
            'partner_id': cls.user_portal.partner_id.id,
            'pricelist_id': cls.pricelist_id1.id,
            'rental_start_date': fields.Datetime.now(),
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=9),
            'order_line': [
                Command.create({
                    'name': 'Test Rental',
                    'product_id': cls.test_rent.id,
                }),
            ]
        })

    def test_rental_pricelist(self):
        self.assertEqual(self.rent_order.order_line[0].price_subtotal, 45)

        self.rent_order.write({
            'rental_start_date': fields.Datetime.now(),
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=1),
        })
        self.rent_order._recompute_prices()
        self.assertEqual(self.rent_order.order_line[0].price_subtotal, 10)

        self.rent_order.write({
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=24),
        })
        self.rent_order._recompute_prices()
        self.assertEqual(self.rent_order.order_line[0].price_subtotal, 100)

        self.rent_order.write({
            'pricelist_id': self.pricelist_id2.id,
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=9),
        })
        self.rent_order._recompute_prices()
        self.assertEqual(self.rent_order.order_line[0].price_subtotal, 40.5)
        self.assertEqual(self.rent_order.order_line[0].discount, 10)

        self.rent_order.write({
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=20),
        })
        self.rent_order._recompute_prices()
        self.assertEqual(self.rent_order.order_line[0].price_subtotal, 90)
