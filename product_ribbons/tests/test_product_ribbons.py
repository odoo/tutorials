from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestSaleRibbon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.product = cls.env["product.template"].search([], limit=1)
        cls.christmas_pricelist = cls.env["product.pricelist"].search(
            [("name", "=", "Christmas")], limit=1
        )
        cls.christmas_pricelist.write({"selectable": True})
        cls.prices = cls.product._get_sales_prices(cls.website)

    def test_pricelist_discount_applies_sale_ribbon(self):
        sale_ribbon = self.env["product.ribbon"].create({
            "name": "Sale",
            "assign": "sale",
        })
        self.product._get_ribbon(self.prices)
        self.assertEqual(
            self.product.website_ribbon_id,
            sale_ribbon,
            "Pricelist discount applied, but Sale Ribbon was not correctly assigned!",
        )

    def test_ribbon_priority_out_of_stock(self):
        self.product.write({"qty_available": 0, "allow_out_of_stock_order": False})
        out_of_stock_ribbon = self.env["product.ribbon"].create({
            "name": "Out of Stock",
            "assign": "out_of_stock",
        })
        self.env["product.ribbon"].create({"name": "Sale", "assign": "sale"})
        self.product._get_ribbon(self.prices)
        self.assertEqual(
            self.product.website_ribbon_id,
            out_of_stock_ribbon,
            " Out of Stock Ribbon not prioritized!",
        )

    def test_duplicate_ribbon_validation(self):
        self.env["product.ribbon"].create({"name": "Sale Discount", "assign": "sale"})
        with self.assertRaises(ValidationError):
            self.env["product.ribbon"].create({"name": "Sale Offer", "assign": "sale"})

    def test_manual_ribbon_priority_over_any(self):
        manual_ribbon = self.env["product.ribbon"].create({
            "name": "Sold Out",
            "assign": "manual",
        })
        self.product.write({"website_ribbon_id": manual_ribbon.id})
        self.env["product.ribbon"].create({"name": "New", "assign": "new"})
        self.product._get_ribbon(self.prices)
        self.assertEqual(
            self.product.website_ribbon_id,
            manual_ribbon,
            " Manual ribbon was replaced by an automatic ribbon!",
        )

    def test_out_of_stock_ribbon_respects_allow_out_of_stock(self):
        out_of_stock_ribbon = self.env["product.ribbon"].create({
            "name": "Out of Stock",
            "assign": "out_of_stock",
        })

        self.product.write({"allow_out_of_stock_order": False, "qty_available": 0})
        self.product._get_ribbon(self.prices)
        self.assertEqual(
            self.product.website_ribbon_id,
            out_of_stock_ribbon,
            " Out of Stock ribbon did NOT apply when allow_out_of_stock_order is False!",
        )

        self.product.write({"allow_out_of_stock_order": True, "qty_available": 0})
        self.product._get_ribbon(self.prices)
        self.assertNotEqual(
            self.product.website_ribbon_id,
            out_of_stock_ribbon,
            " Out of Stock ribbon incorrectly applied when allow_out_of_stock_order is True!",
        )
