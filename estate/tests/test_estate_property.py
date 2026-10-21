from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged


class EstatePropertyTestCase(TransactionCase):
    _test_user_groups = ("base.group_user",)
    _test_user_name = "Test User"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_types = cls.env["estate.property.type"].create(
            [
                {
                    "name": "House",
                    "sequence": 1,
                },
                {
                    "name": "Castle",
                    "sequence": 2,
                },
            ]
        )

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "sold_property",
                    "expected_price": 10_000,
                    "living_area": 100,
                    "property_type_id": cls.property_types[0].id,
                    "state": "sold",
                },
                {
                    "name": "offered_property",
                    "expected_price": 10_000,
                    "living_area": 100,
                    "property_type_id": cls.property_types[1].id,
                    "state": "new",
                },
            ]
        )

    @tagged("post_install")
    def test_cannot_create_offer_on_sold_property(self):
        """Test that we cannot create an offer on property that is sold"""
        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "price": 10_000,
                        "partner_id": self.env.user.id,
                        "property_id": self.properties[0].id,
                    }
                ]
            )

    @tagged("post_install")
    def test_cannot_sell_property_with_no_accepted_offers(self):
        self.env["estate.property.offer"].create(
            [
                {
                    "price": 10_000,
                    "partner_id": self.env.user.id,
                    "property_id": self.properties[1].id,
                }
            ]
        )

        self.assertEqual(
            self.properties[1].state,
            "offer_received",
            "Adding offer to property did not change state to 'offer_received'",
        )

        with self.assertRaises(ValidationError):
            self.properties[1].sold_property()

    @tagged("post_install")
    def test_garden_onchange_works(self):
        form = Form(self.properties[0])
        self.assertTrue(
            form._get_modifier("garden_area", "invisible"),
            "garden area should be invisible",
        )
        form.garden = True
        self.assertEqual(form.garden_area, 10)
        self.assertEqual(form.garden_orientation, "north")
