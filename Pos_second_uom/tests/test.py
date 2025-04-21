from odoo.tests.common import TransactionCase


class TestPOSSecondaryUoM(TransactionCase):

    def setUp(self):
        super().setUp()

        self.uom_category = self.env['uom.category'].create({
            'name': 'Custom UoM Category',
        })

        self.uom_unit = self.env['uom.uom'].create({
            'name': 'Unit',
            'category_id': self.uom_category_id,
            'factor_inv': 1.0,
            'uom_type': 'reference',
        })

        self.uom_drozen = self.env['uom.uom'].create({
            'name': 'DROZENS',
            'category_id': self.uom_category_id,
            'factor_inv': 12.0,
            'uom_type': 'bigger',
        })

        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
            'pos_secondary_uom_id': self.uom_drozen.id,
        })

        self.pos_session = self.env['pos.session'].search([], limit=1)
        if not self.pos_session:
            config = self.env['pos.config'].create({'name': 'Test POS Config'})
            self.pos_session = self.env['pos.session'].create({'config_id': config.id})

    def test_pos_quantity_conversion_from_secondary_uom(self):
        """When entering 0.5 DROZEN, the quantity in Unit should be 6."""

        qty_in_secondary = 0.5
        expected_qty_in_units = qty_in_secondary * self.uom_drozen.factor_inv

        pos_order = self.env['pos.order'].create({
            'session_id': self.pos_session.id,
            'lines': [(0, 0, {
                'product_id': self.product.id,
                'qty': expected_qty_in_units,
                'price_unit': self.product.list_price,
            })]
        })

        line = pos_order.lines[0]
        self.assertEqual(
            line.qty, 6.0,
            "Expected 0.5 DROZEN to convert to 6 Units in POS order line."
        )
