from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env["estate.property"].create(
            {"name": "property1", "state": "new", "expected_price": 100}
        )

    def test_create_offer_for_sold_property(self):
        property = self.env["estate.property"].create(
            {"name": "property1", "state": "sold", "expected_price": 100}
        )
        self.env["estate.property.offer"].create(
            {
                "price": 90000,
                "property_id": property.id,
                "partner_id": self.env.ref("base.res_partner_12").id,
            }
        )

    def test_sell_property_with_no_accepted_offer(self):
        property = self.env["estate.property"].create(
            {"name": "property2", "state": "new", "expected_price": 100}
        )
        property.action_set_sold()
