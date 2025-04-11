from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestProductribbon(TransactionCase):

    def setUp(self):
        super().setUp()
        self.website = self.env["website"].search([], limit=1)
        self.product = self.env["product.template"].search([], limit=1)
        self.christmas_pricelist = self.env["product.pricelist"].search(
            [("name", "=", "Christmas")], limit=1
        )
        self.christmas_pricelist.write({"selectable": True})
        self.prices = self.product._get_sales_prices(self.website)

    def _create_ribbon(self, name, assign):
        return self.env["product.ribbon"].create({
            "name": name,
            "assign": assign,
        })

    def test_sale_ribbon_is_assigned_when_discount_applies(self):
        ribbon = self._create_ribbon("Sale", "sale")
        self.product._get_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            "Expected Sale ribbon to be assigned when pricelist discount is active."
        )

    def test_out_of_stock_ribbon_priority_over_sale(self):
        self.product.write({
            "qty_available": 0,
            "allow_out_of_stock_order": False
        })

        out_ribbon = self._create_ribbon("Out of Stock", "out_of_stock")
        self._create_ribbon("Sale", "sale")
        self.product._get_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            out_ribbon.id,
            "Out of Stock ribbon should take priority over Sale ribbon."
        )

    def test_validation_error_on_duplicate_ribbon_assign(self):
        self._create_ribbon("Sale Discount", "sale")
        with self.assertRaises(ValidationError, msg="Duplicate 'sale' ribbon should raise ValidationError"):
            self._create_ribbon("Sale Offer", "sale")

    def test_manual_ribbon_should_override_automatic(self):
        manual = self._create_ribbon("Sold Out", "manual")
        self.product.write({"website_ribbon_id": manual.id})
        self._create_ribbon("New", "new")

        self.product._get_ribbon(self.prices)

        self.assertEqual(
            self.product.website_ribbon_id.id,
            manual.id,
            "Manual ribbon must not be replaced by any automatic ribbon."
        )

    def test_out_of_stock_respects_allow_out_of_stock_flag(self):
        ribbon = self._create_ribbon("Out of Stock", "out_of_stock")

        # Case 1: Should apply
        self.product.write({"qty_available": 0, "allow_out_of_stock_order": False})
        self.product._get_ribbon(self.prices)
        self.assertEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            "Expected Out of Stock ribbon when allow_out_of_stock_order is False."
        )

        # Case 2: Should NOT apply
        self.product.write({"allow_out_of_stock_order": True})
        self.product._get_ribbon(self.prices)
        self.assertNotEqual(
            self.product.website_ribbon_id.id,
            ribbon.id,
            "Out of Stock ribbon should not be shown when allow_out_of_stock_order is True."
        )
