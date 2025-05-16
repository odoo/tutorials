from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged("post_install", "-at_install")
class EstateTest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env["estate.property"].create(
            {"name": "dlf camellias", "expected_price": 1000000000}
        )
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.offer = cls.env["estate.property.offer"].create(
            {
                "partner_id": cls.partner.id,
                "property_id": cls.property.id,
                "price": 1000000000,
                "validity": 14,
            }
        )

    def test_selling_property_with_no_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.set_as_sold()

    def test_create_offer_for_sold_property(self):
        self.offer.status = "accepted"
        self.property.set_as_sold()
        self.assertRecordValues(
            self.property, [{"name": "dlf camellias", "state": "sold"}]
        )

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "partner_id": self.partner.id,
                    "property_id": self.property.id,
                    "price": 1000000000,
                    "validity": 15,
                }
            )

    def test_reset_garden(self):
        with Form(self.property) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(
                form.garden_orientation, "north"
            )  # To check that our onchange is working find and changing garden_area and garden_orientation
            form.garden = False
            self.assertEqual(
                form.garden_area,
                0,
                "Garden Area should be reset to 0 when Garden checkbox is unchecked",
            )
            self.assertEqual(
                form.garden_orientation,
                False,
                "Garden Orientation should be reset to False when Garden checkbox is unchecked",
            )
