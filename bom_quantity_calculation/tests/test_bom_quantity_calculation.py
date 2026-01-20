import math

from odoo.tests.common import TransactionCase


class TestBomQuantityCalculation(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a product with a specific_weight
        cls.product_1 = cls.env['product.product'].create({
            'name': 'Product 1',
            'type': 'consu',
            'specific_weight': 7.85,
        })
        # Create a second product for the BOM
        cls.product_2 = cls.env['product.product'].create({
            'name': 'Product 2',
            'type': 'consu',
        })
        # Create a BOM for the second product
        cls.bom = cls.env['mrp.bom'].create({
            'product_tmpl_id': cls.product_2.product_tmpl_id.id,
        })
        # Add the first product as a BOM line
        cls.bom_line = cls.env['mrp.bom.line'].create({
            'product_id': cls.product_1.id,
            'bom_id': cls.bom.id,
        })

    def test_qty_computation_diameter_length(self):
        """Test product_qty computation using diameter and length."""
        self.bom_line.write({
            'diameter': 20,
            'length': 1000,
        })

        self.bom_line._compute_product_qty()

        expected_qty = (
            3.14159 * ((20 ** 2) / 4) * 1000 / 1000000
        ) * 7.85
        self.assertEqual(
            self.bom_line.product_qty,
            math.floor(expected_qty),
        )

    def test_qty_computation_length_width_thickness(self):
        """Test product_qty computation using length, width, and thickness."""
        self.bom_line.write({
            'length': 2000,
            'width': 100,
            'thickness': 10,
        })

        self.bom_line._compute_product_qty()

        expected_qty = (
            (2000 * 100 * 10 / 1000000)
        ) * 7.85
        self.assertEqual(
            self.bom_line.product_qty,
            math.floor(expected_qty),
        )
