from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestOfferCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        cls.property_sold = cls.env["estate.property"].create(
            {"name": "Sold Property", "expected_price": 31, "state": "sold"}
        )

    def test_create_offer_on_sold_property(self):
        """Test that we can't create an offer for a sold property"""
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 67,
                    "partner_id": self.env.user.partner_id.id,
                    "property_id": self.property_sold.id,
                }
            )
