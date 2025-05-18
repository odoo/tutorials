from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form


class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env["estate.property"].create([
            {
                "name": "Hello Villa",
                "expected_price": 100000,
                "living_area": 100,
                "garden": True,
                "garden_area": 50,
                "state": "offer_accepted",
            },
        ])

        cls.offers = cls.env["estate.property.offer"].create([
            {
                "property_id": cls.properties[0].id,
                "partner_id": cls.env.ref("base.res_partner_12").id,
                "price": 5000,
                "status": "accepted",
            }
        ])

    def test_creation_area(self):
        self.assertEqual(
            self.properties[0].total_area,
            150,
            "Total area should be the sum of garden area and living area",
        )

    def test_action_sell(self):
        self.properties[0].action_sold_property()
        self.assertEqual(
            self.properties[0].state,
            "sold",
            "The property state should update on pressing sell button",
        )

    def test_add_offer_for_sold_property(self):
        self.properties[0].write({"state": "sold"})
        with self.assertRaises(
            UserError, msg="You cannot create offer for a sold property"
        ):
            self.env["estate.property.offer"].create({
                "property_id": self.properties[0].id,
                "partner_id": self.env.ref("base.res_partner_12").id,
                "price": 7000,
            })

    def test_sell_a_property_with_no_accepted_offers(self):
        self.properties[0].offer_ids.write({"status": "refused"})
        accepted_offers = self.properties[0].offer_ids.filtered(
            lambda offer: offer.status == "accepted"
        )
        self.assertFalse(accepted_offers, "There should be no accepted offers")

        with self.assertRaises(
            UserError, msg="Expected UserError when selling without accepted offers"
        ):
            self.properties[0].action_sold_property()

    def test_garden_field_behavior(self):
        property_form = Form(self.env["estate.property"])
        property_form.name = "Big House"
        property_form.expected_price = 10000
        property_form.garden = True
        property_form.garden_area = 50
        property_form.garden_orientation = "north"

        property = property_form.save()

        with Form(property) as property_form:
            property_form.garden = False
            property = property_form.save()

        self.assertEqual(property.garden_area, 0, "Garden Area was reset unexpectedly")
        self.assertEqual(
            property.garden_orientation, False, "Orientation was reset unexpectedly"
        )
