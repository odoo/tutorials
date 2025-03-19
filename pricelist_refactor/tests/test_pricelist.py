from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import tagged
from odoo.fields import Command
from odoo.tests.common import TransactionCase

@tagged('post_install', '-at_install')
class TestPricelist(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Test user
        TestUsersEnv = cls.env['res.users'].with_context({'no_reset_password': True})
        group_portal_id = cls.env.ref('base.group_portal').id
        cls.country_belgium = cls.env.ref('base.be')
        cls.user_portal = TestUsersEnv.create({
            'name': 'Beatrice Portal',
            'login': 'Beatrice',
            'country_id': cls.country_belgium.id,
            'email': 'beatrice.employee@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
        })

        # Test subscription plan
        cls.sub_monthly_plan = cls.env['sale.subscription.plan'].create({
            'name': 'Monthly Plan',
            'billing_period_value': 1,
            'billing_period_unit': 'month'
        })
        cls.sub_yearly_plan = cls.env['sale.subscription.plan'].create({
            'name': 'Yearly Plan',
            'billing_period_value': 1,
            'billing_period_unit': 'year'
        })

        # Test rental period
        cls.recurrence_hourly = cls.env['sale.temporal.recurrence'].create({'duration': 1.0, 'unit': 'hour'})
        cls.recurrence_daily = cls.env['sale.temporal.recurrence'].create({'duration': 1.0, 'unit': 'day'})

        # Test products
        cls.sub_product_tmpl = cls.env['product.template'].create({
            'name': 'BaseTestProduct',
            'type': 'service',
            'recurring_invoice': True,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
        })
        cls.test_sub = cls.sub_product_tmpl.product_variant_id
        cls.test_rent = cls.env['product.product'].create({
            'name': 'Projector',
            'rent_ok': True,
            'extra_hourly': 7.0,
            'extra_daily': 30.0,
        })
        cls.test_rent_template_id = cls.test_rent.product_tmpl_id

        # Test pricelists
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Pricelist',
        })

        cls.pricelist_id1 = cls.env['product.pricelist'].create({
            'name': 'Subscription pricelist 1',
            'product_subscription_pricelist_ids': [
                Command.create({
                    'compute_price': 'fixed',
                    'plan_id': cls.sub_monthly_plan.id,
                    'fixed_price': 100,
                    'product_tmpl_id': cls.sub_product_tmpl.id,
                    'applied_on': '1_product',
                }),
                Command.create({
                    'compute_price': 'fixed',
                    'plan_id': cls.sub_yearly_plan.id,
                    'fixed_price': 1000,
                    'product_tmpl_id': cls.sub_product_tmpl.id,
                    'applied_on': '1_product',
                }),
            ],
            'product_rental_pricelist_ids': [
                Command.create({
                    'compute_price': 'fixed',
                    'recurrence_id': cls.recurrence_hourly.id,
                    'fixed_price': 10,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product'
                }),
                Command.create({
                    'compute_price': 'fixed',
                    'recurrence_id': cls.recurrence_daily.id,
                    'fixed_price': 100,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product'
                })
            ],
        })
        cls.pricelist_id2 = cls.env['product.pricelist'].create({
            'name': 'Subscription pricelist 2',
            'product_subscription_pricelist_ids': [
                Command.create({
                    'compute_price': 'percentage',
                    'plan_id': cls.sub_monthly_plan.id,
                    'percent_price': 10,
                    'base': 'pricelist',
                    'base_pricelist_id': cls.pricelist_id1.id,
                    'product_tmpl_id': cls.sub_product_tmpl.id,
                    'applied_on': '1_product',
                }),
                Command.create({
                    'compute_price': 'formula',
                    'plan_id': cls.sub_yearly_plan.id,
                    'base': 'pricelist',
                    'base_pricelist_id': cls.pricelist_id1.id,
                    'price_surcharge': -0.5,
                    'product_tmpl_id': cls.sub_product_tmpl.id,
                    'applied_on': '1_product',
                }),
            ],
            'product_rental_pricelist_ids': [
                Command.create({
                    'compute_price': 'percentage',
                    'recurrence_id': cls.recurrence_hourly.id,
                    'percent_price': 10,
                    'base': 'pricelist',
                    'base_pricelist_id': cls.pricelist_id1.id,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product'
                }),
                Command.create({
                    'compute_price': 'formula',
                    'recurrence_id': cls.recurrence_daily.id,
                    'base': 'pricelist',
                    'base_pricelist_id': cls.pricelist_id1.id,
                    'price_surcharge': -10,
                    'product_tmpl_id': cls.test_rent_template_id.id,
                    'applied_on': '1_product'
                })
            ]
        })

        # Test subscription orders
        cls.subscription_order = cls.env['sale.order'].create({
            'name' : 'Test Subscription',
            'is_subscription': True,
            'plan_id': cls.sub_monthly_plan.id,
            'partner_id': cls.user_portal.partner_id.id,
            'pricelist_id': cls.pricelist_id1.id,
            'order_line': [
                Command.create({
                    'name': 'Test Subscription',
                    'product_id': cls.test_sub.id,
                }),
            ]
        })

        # Test rental orders
        cls.rent_order = cls.env['sale.order'].create({
            'name' : 'Test Rental',
            'partner_id': cls.user_portal.partner_id.id,
            'pricelist_id': cls.pricelist_id1.id,
            'rental_start_date': fields.Datetime.now(),
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=9),
        })

        cls.rent_order.write({
            'order_line': [
                Command.create({
                    'name': 'Test Rental',
                    'product_id': cls.test_rent.id,
                }),
            ]
        })

    def test_subscription_pricelist(self):

        self.assertEqual(
            self.subscription_order.order_line[0].price_subtotal,
            100
        )

        self.subscription_order.write({
            'plan_id': self.sub_yearly_plan.id
        })
        self.subscription_order._recompute_prices()
        self.assertEqual(
            self.subscription_order.order_line[0].price_subtotal,
            1000
        )

        self.subscription_order.write({
            'pricelist_id': self.pricelist_id2.id
        })
        self.subscription_order._recompute_prices()
        self.assertEqual(
            self.subscription_order.order_line[0].price_subtotal,
            999.5
        )

        self.subscription_order.write({
            'plan_id': self.sub_monthly_plan.id
        })
        self.subscription_order._recompute_prices()
        self.assertEqual(
            self.subscription_order.order_line[0].discount,
            10
        )
        self.assertEqual(
            self.subscription_order.order_line[0].price_subtotal,
            90
        )

    def test_rental_pricelist(self):

        self.assertEqual(
            self.rent_order.order_line[0].price_subtotal,
            90
        )

        self.rent_order.write({
            'rental_start_date': fields.Datetime.now(),
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=24),
        })
        self.rent_order._recompute_prices()
        self.assertEqual(
            self.rent_order.order_line[0].price_subtotal,
            100
        )

        self.rent_order.write({
            'rental_start_date': fields.Datetime.now(),
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=9),
            'pricelist_id': self.pricelist_id2.id
        })
        self.rent_order._recompute_prices()
        self.assertEqual(
            self.rent_order.order_line[0].price_subtotal,
            81
        )
        self.assertEqual(
            self.rent_order.order_line[0].discount,
            10
        )

        self.rent_order.write({
            'rental_start_date': fields.Datetime.now(),
            'rental_return_date': fields.Datetime.now() + relativedelta(hours=11),
        })
        self.rent_order._recompute_prices()
        self.assertEqual(
            self.rent_order.order_line[0].price_subtotal,
            90
        )
