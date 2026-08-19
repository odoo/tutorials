from odoo.addons.estate.tests.test_estate_offer import TestEstateOffer
from odoo.exceptions import UserError
from odoo.tests import Form, HttpCase, tagged


class TestEstateProperty(TestEstateOffer):
    def test_sell_accepted_offers(self):
        self.env["estate.offer"].create(
            {
                "partner_id": self.env.user.id,
                "property_id": self.property.id,
                "status": "accepted",
            }
        )

        self.property.action_state_sold()
        self.assertEqual(self.property.state, "sold")

    def test_sell_no_accepted_offers(self):
        with self.assertRaises(UserError):
            self.property.action_state_sold()


@tagged("post_install", "-at_install")
class TestEstatePropertyHttp(HttpCase):
    def test_garden_reset(self):
        form = Form(self.env["estate.property"])

        form.garden = True
        self.assertEqual(form.garden_area, 10)
        self.assertEqual(form.garden_orientation, "north")

        form.garden = False
        self.assertEqual(form.garden_area, 0)
        self.assertEqual(form.garden_orientation, False)
