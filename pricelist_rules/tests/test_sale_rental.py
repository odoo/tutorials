# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError

@tagged('-at_install', 'post_install')
class TestRentalPricingRules(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category_rental = cls.env['product.category'].create({'name': "Rental Items"})

        cls.banquet_hall = cls.env['product.product'].create({
            'name': "Banquet Hall",
            'categ_id': cls.category_rental.id,
            'standard_price': 5000,
            'list_price': 7000,
            'rent_ok': True,
        })

        cls.exhibition_center = cls.env['product.product'].create({
            'name': "Exhibition Center",
            'categ_id': cls.category_rental.id,
            'standard_price': 6000,
            'list_price': 8000,
            'rent_ok': True,
        })

        cls.daily_recurrence = cls.env['sale.temporal.recurrence'].create({'name': "Daily", 'duration': 1, 'unit': 'day'})
        cls.weekly_recurrence = cls.env['sale.temporal.recurrence'].create({'name': "Weekly", 'duration': 1, 'unit': 'week'})
        
        cls.pricelist = cls.env['product.pricelist'].create({'name': "Rental Price List"})

    def test_create_pricing_rule_for_product(self):
        pricing_rule = self.env['product.pricing'].create({
            'display_applied_on': '1_product',
            'product_tmpl_id': self.banquet_hall.product_tmpl_id.id,
            'compute_price': 'percentage',
            'base': 'list_price',
            'percent_price': 15,
            'min_quantity': 3,
            'recurrence_id': self.daily_recurrence.id,
            'pricelist_id': self.pricelist.id
        })
        
        self.assertEqual(pricing_rule.product_id, self.banquet_hall, "Product-specific pricing rule not applied correctly")

    def test_create_pricing_rule_for_category(self):
        pricing_rule = self.env['product.pricing'].create({
            'display_applied_on': '2_product_category',
            'categ_id': self.category_rental.id,
            'compute_price': 'fixed',
            'fixed_price': 25000,
            'min_quantity': 5,
            'recurrence_id': self.weekly_recurrence.id,
            'pricelist_id': self.pricelist.id
        })

        self.assertEqual(pricing_rule.categ_id, self.category_rental, "Category-specific pricing rule not created correctly")

    def test_error_on_missing_product_or_category(self):
        with self.assertRaises(UserError, msg="Expected error when product or category is not set"):
            self.env['product.pricing'].create({
                'display_applied_on': '1_product',
                'product_tmpl_id': None,
                'compute_price': 'fixed',
                'fixed_price': 10000,
                'min_quantity': 2,
                'recurrence_id': self.daily_recurrence.id,
                'pricelist_id': self.pricelist.id
            })

        with self.assertRaises(UserError, msg="Expected error when category is missing"):
            self.env['product.pricing'].create({
                'display_applied_on': '2_product_category',
                'categ_id': None,
                'compute_price': 'fixed',
                'fixed_price': 15000,
                'min_quantity': 4,
                'recurrence_id': self.weekly_recurrence.id,
                'pricelist_id': self.pricelist.id
            })
