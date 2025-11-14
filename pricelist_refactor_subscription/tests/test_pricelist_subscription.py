from odoo.fields import Command
from ...pricelist_refactor_base.tests.test_pricelist_base import TestPricelistBase


class TestPricelistSubscription(TestPricelistBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sub_monthly_plan = cls.env['sale.subscription.plan'].create({
            'name': 'Monthly Plan',
            'billing_period_value': 1,
            'billing_period_unit': 'month',
        })
        cls.sub_yearly_plan = cls.env['sale.subscription.plan'].create({
            'name': 'Yearly Plan',
            'billing_period_value': 1,
            'billing_period_unit': 'year',
        })

        cls.sub_product_tmpl = cls.env['product.template'].create({
            'name': 'Base Subscription Product',
            'type': 'service',
            'recurring_invoice': True,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
        })
        cls.test_sub = cls.sub_product_tmpl.product_variant_id

        cls.pricelist_id1 = cls.env['product.pricelist'].create({
            'name': 'Subscription Pricelist 1',
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
        })

        cls.pricelist_id2 = cls.env['product.pricelist'].create({
            'name': 'Subscription Pricelist 2',
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
        })

        cls.subscription_order = cls.env['sale.order'].create({
            'name': 'Test Subscription',
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

    def test_subscription_pricelist(self):
        self.assertEqual(self.subscription_order.order_line[0].price_subtotal, 100)

        self.subscription_order.write({'plan_id': self.sub_yearly_plan.id})
        self.subscription_order._recompute_prices()
        self.assertEqual(self.subscription_order.order_line[0].price_subtotal, 1000)

        self.subscription_order.write({'pricelist_id': self.pricelist_id2.id})
        self.subscription_order._recompute_prices()
        self.assertEqual(self.subscription_order.order_line[0].price_subtotal, 999.5)

        self.subscription_order.write({'plan_id': self.sub_monthly_plan.id})
        self.subscription_order._recompute_prices()
        self.assertEqual(self.subscription_order.order_line[0].discount, 10)
        self.assertEqual(self.subscription_order.order_line[0].price_subtotal, 90)
