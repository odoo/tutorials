from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


class TestSecondUom(TestPointOfSaleHttpCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.dozen_uom = self.env.ref("uom.product_uom_dozen")
        self.unit_uom = self.env.ref("uom.product_uom_unit")
        self.product = self.env["product.product"].create({
            "name": "Test Product",
            "uom_id": self.dozen_uom.id,
            "second_uom_id": self.unit_uom.id,
            "lst_price": 12.0,
            "pos_categ_ids": [(6, None, [8])]
        })
        self.main_pos_config = self.env["pos.config"].create({
            "name": "Test POS Config",
        })
        self.tip = self.env.ref('point_of_sale.product_product_tip')

    def test_add_quantity_in_second_uom_tour(self):
        self.tip.write({
            'taxes_id': False
        })
        self.main_pos_config.write({
            'iface_tipproduct': True,
            'tip_product_id': self.tip.id,
            'ship_later': True
        })
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.env['ir.module.module'].search([('name', '=', 'point_of_sale_second_uom')], limit=1).state = 'installed'

        self.start_pos_tour('SecondUomTour', watch=True,step_delay=1500)
