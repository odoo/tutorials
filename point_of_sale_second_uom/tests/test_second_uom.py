from odoo.tests.common import TransactionCase

class TestSecondUom(TransactionCase):
    def setUp(self):
        super(TestSecondUom, self).setUp()
        self.dozen_uom = self.env.ref("uom.product_uom_dozen")
        self.unit_uom = self.env.ref("uom.product_uom_unit")
        self.product = self.env["product.product"].create({
            "name": "Test Product",
            "uom_id": self.dozen_uom.id,
            "second_uom_id": self.unit_uom.id,
            "lst_price": 12.0,
        })
        self.pos_config = self.env["pos.config"].create({
            "name": "Test POS Config",
        })
        self.pos_session = self.env["pos.session"].create({
            "config_id": self.pos_config.id,
        })

        self.order = self.env["pos.order"].create({
            "name": "Test Order",
            "session_id": self.pos_session.id,
            "amount_total": 0.0,
            "amount_tax": 0.0,
            "amount_paid": 0.0,
            "amount_return": 0.0,
        })
        self.order_line = self.env["pos.order.line"].create({
            "order_id": self.order.id,
            "product_id": self.product.id,
            "qty": 1,
            "price_unit": self.product.lst_price,
            "price_subtotal": 0.0,
            "price_subtotal_incl": 0.0,
        })

    def test_add_quantity_in_second_uom(self):
        """Test adding quantity in the second UoM and updating the primary UoM."""
        second_uom_qty = 6
        expected_primary_uom_qty = second_uom_qty * (self.dozen_uom.factor/self.unit_uom.factor)

        self.order_line.qty = expected_primary_uom_qty
        self.assertEqual(
            self.order_line.qty,
            0.5,
        )
