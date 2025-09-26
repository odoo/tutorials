from odoo.tests import tagged
from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon

@tagged('post_install', '-at_install')
class TestPOS(TestPointOfSaleHttpCommon):

    def setUp(self):
        super().setUp()

        self.uom_category_unit = self.env['uom.category'].create({
            'name': 'Unit Category'
        })

        self.uom_unit = self.env['uom.uom'].create({
            'name': 'Unit',
            'category_id': self.uom_category_unit.id,
            'uom_type': 'reference',
            'factor_inv': 1.0,
            'rounding': 0.01,
        })

        self.uom_dozen = self.env['uom.uom'].create({
            'name': 'Dozen',
            'category_id': self.uom_category_unit.id,
            'uom_type': 'smaller',
            'factor_inv': 12.0,
            'rounding': 0.01,
        })

        self.letter_tray = self.env['product.product'].create({
            'name': 'Apple',
            'uom_id': self.uom_dozen.id,
            'uom_po_id': self.uom_dozen.id,
            'second_uom_id': self.uom_unit.id,
            'available_in_pos': True,
            'list_price': 12.0,
        })
        
        # self.main_pos_config.x = [(4, self.letter_tray.id)]

    def test_pos_uom_conversion_tour(self):
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_tour("/pos/ui?config_id=%d" % self.main_pos_config.id, 'pos_uom_conversion', login="pos_user", watch=True)
