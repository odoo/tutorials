from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSecondUomConversion(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.uom_dozen = cls.env.ref('uom.product_uom_dozen')
        cls.uom_dozen.write({'active': True})

        cls.test_product = cls.env['product.template'].create({
            'name': 'Premium Eggs Box',
            'type': 'consu',
            'uom_id': cls.uom_dozen.id,
            'pos_second_uom_id': cls.uom_unit.id,
            'list_price': 10.0,
        })

    def test_second_uom_is_set_on_product(self):
        self.assertEqual(self.test_product.pos_second_uom_id, self.uom_unit)

    def test_6_units_converts_to_0_5_dozen(self):
        """core requirement: entering 6 units maps to 0.5 dozen"""
        entered_qty = 6.0
        converted = (entered_qty * self.uom_unit.relative_factor) / self.uom_dozen.relative_factor
        self.assertAlmostEqual(converted, 0.5)

    def test_12_units_converts_to_1_dozen(self):
        entered_qty = 12.0
        converted = (entered_qty * self.uom_unit.relative_factor) / self.uom_dozen.relative_factor
        self.assertAlmostEqual(converted, 1.0)

    def test_second_uom_cleared_when_incompatible_uom_set(self):
        uom_hour = self.env.ref('uom.product_uom_hour')

        self.test_product.uom_id = uom_hour.id
        self.test_product._onchange_uom_id_clear_second()

        self.assertFalse(self.test_product.pos_second_uom_id)
