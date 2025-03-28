# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError

@tagged('-at_install', 'post_install')
class TestSubscriptionPricing(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = cls.env['product.category'].create({'name': "Digital Services"})
        cls.pricelist = cls.env['product.pricelist'].create({'name': "Service Pricelist"})

        cls.video_streaming_basic = cls.env['product.product'].create({
            'name': "Video Streaming Basic Plan",
            'categ_id': cls.category.id,
            'standard_price': 8000,
            'list_price': 10000,
            'recurring_invoice': True,
        }).product_tmpl_id

        cls.plan_weekly = cls.env['sale.subscription.plan'].create({
            'name': "Weekly",
            'billing_period_value': 1,
            'billing_period_unit': 'week'
        })

    def test_create_pricing_rule_by_product(self):
        pricing_rule = self.env['sale.subscription.pricing'].create({
            'display_applied_on': '1_product',
            'product_tmpl_id': self.video_streaming_basic.id,
            'compute_price': 'percentage',
            'base': 'list_price',
            'price': 120,
            'percent_price': 15,
            'min_quantity': 3,
            'plan_id': self.plan_weekly.id,
            'pricelist_id': self.pricelist.id
        })
        self.assertEqual(pricing_rule.product_tmpl_id.id, self.video_streaming_basic.id, "Product-based pricing rule not created correctly")

    def test_error_missing_product_or_category(self):
        with self.assertRaises(UserError, msg="You cannot create a subscription-based rule for a non-subscribable category."):
            self.env['sale.subscription.pricing'].create({
                'display_applied_on': '2_product_category',
                'categ_id': None,
                'compute_price': 'fixed',
                'fixed_price': 18000,
                'min_quantity': 4,
                'plan_id': self.plan_weekly.id,
                'pricelist_id': self.pricelist.id
            })

    def test_error_duplicate_pricing_rule(self):
        self.env['sale.subscription.pricing'].create({
            'display_applied_on': '1_product',
            'product_tmpl_id': self.video_streaming_basic.id,
            'compute_price': 'percentage',
            'price': 120,
            'percent_price': 15,
            'min_quantity': 3,
            'plan_id': self.plan_weekly.id,
            'pricelist_id': self.pricelist.id
        })

        with self.assertRaises(UserError, msg="A pricing already exists for this product, plan, and pricelist."):
            self.env['sale.subscription.pricing'].create({
                'display_applied_on': '1_product',
                'product_tmpl_id': self.video_streaming_basic.id,
                'compute_price': 'percentage',
                'price': 120,
                'percent_price': 15,
                'min_quantity': 3,
                'plan_id': self.plan_weekly.id,
                'pricelist_id': self.pricelist.id
            })
