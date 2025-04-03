# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase
from odoo.tests.common import tagged


@tagged('post_install', '-at_install')
class TestWebsiteProductUoM(TransactionCase):

    def setUp(self):
        super().setUp()

        self.uom_unit_category = self.env['uom.category'].create({'name': 'Test Units'})
        self.uom_weight_category = self.env['uom.category'].create({'name': 'Test Weight'})
        self.uom_unit = self.env['uom.uom'].create({
            'name': 'Test Unit',
            'category_id': self.uom_unit_category.id,
            'uom_type': 'reference',
            'factor': 1.0,
            'rounding': 0.01
        })
        self.uom_dozen = self.env['uom.uom'].create({
            'name': 'Test Dozen',
            'category_id': self.uom_unit_category.id,
            'uom_type': 'bigger',
            'factor': 0.083333,
            'rounding': 0.01
        })
        self.uom_kg = self.env['uom.uom'].create({
            'name': 'Test Kg',
            'category_id': self.uom_weight_category.id,
            'uom_type': 'reference',
            'factor': 1.0,
            'rounding': 0.001
        })
        self.test_product = self.env['product.template'].create({
            'name': 'Test Product',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'website_uom_id': self.uom_unit.id
        })

    def test_compute_uom_category(self):
        """Test computation of uom_category_id based on uom_id"""
        self.assertEqual(self.test_product.uom_category_id, self.uom_unit_category,
                        "Initial UoM category should match the unit category")
        self.test_product.write({
            'website_uom_id': self.uom_kg.id,
            'uom_id': self.uom_kg.id
        })
        self.assertEqual(self.test_product.uom_category_id, self.uom_weight_category,
                        "UoM category should be updated when UoM changes")

    def test_website_uom_constraint_valid(self):
        """Test valid website UoM assignment from same category"""
        self.test_product.website_uom_id = self.uom_dozen
        self.assertEqual(self.test_product.website_uom_id, self.uom_dozen,
                        "Should allow website UoM from same category")

    def test_website_uom_constraint_invalid(self):
        """Test invalid website UoM assignment from different category"""
        with self.assertRaises(ValidationError):
            self.test_product.website_uom_id = self.uom_kg

    def test_onchange_uom_id(self):
        """Test onchange behavior when changing uom_id"""
        self.test_product.website_uom_id = self.uom_dozen
        test_product = self.env['product.template'].with_context(
            default_website_uom_id=self.uom_dozen.id
        ).new({
            'uom_id': self.uom_unit.id,
            'website_uom_id': self.uom_dozen.id
        })
        test_product.uom_id = self.uom_kg
        result = test_product._onchange_uom_id()
        self.assertFalse(test_product.website_uom_id,
                        "website_uom_id should be cleared when uom_id category changes")
        self.assertTrue(result and 'warning' in result,
                       "Onchange should return warning when clearing website_uom_id")

    def test_default_website_uom(self):
        """Test default value of website_uom_id"""
        new_product = self.env['product.template'].create({
            'name': 'New Test Product',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'website_uom_id': self.uom_unit.id
        })
        self.assertEqual(new_product.website_uom_id, self.uom_unit,
                        "website_uom_id should be set to the specified value")

    def test_change_uom_category_flow(self):
        """Test the complete flow of changing UoM category"""
        self.test_product.uom_id = self.uom_unit
        self.test_product.website_uom_id = self.uom_dozen
        self.assertEqual(self.test_product.uom_category_id, self.uom_unit_category)
        self.assertEqual(self.test_product.website_uom_id, self.uom_dozen)
        self.test_product.write({
            'website_uom_id': self.uom_kg.id,
            'uom_id': self.uom_kg.id
        })
        self.assertEqual(self.test_product.uom_category_id, self.uom_weight_category)
        self.assertEqual(self.test_product.website_uom_id, self.uom_kg)
        with self.assertRaises(ValidationError):
            self.test_product.website_uom_id = self.uom_dozen
