from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env["estate.property"].create(
            {"name": "property1", "state": "new", "expected_price": 100}
        )
        cls.offer=cls.env["estate.property.offer"].create(
            {
                "price": 90000,
                "property_id": property.id,
                "partner_id": cls.env.ref("base.res_partner_12").id,
            }
        )

    def test_sell_property_with_no_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.set_as_sold()

    def test_create_offer_for_sold_property(self):
        self.offer.status = "accepted"
        self.property.set_as_sold()
        self.assertRecordValues(
            self.property, [{"name": "sre2 property", "state": "sold"}]
        )
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.partner.id,
                    "property_id": self.property.id,
                    "price": 100,
                }
            )

    def test_onchange_garden(self):
        with Form(self.property) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(
                form.garden_orientation, "north"
            )
            form.garden = False
            self.assertEqual(
                form.garden_area,
                0,
                "garden checkbox is unchecked",
            )
            self.assertEqual(
                form.garden_orientation,
                False,
                "garden checkbox is unchecked",
            )
