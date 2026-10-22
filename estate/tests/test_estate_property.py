from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase, tagged


class EstatePropertyTestCase(TransactionCase):
    _test_user_groups = ("base.group_user",)
    _test_user_name = "Test User"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.dummy_user = cls.env["res.partner"].create(
            {
                "name": "Test User",
                "email": "test_user@example.com",
            }
        )

        cls.type_house, cls.type_castle = cls.property_types = cls.env[
            "estate.property.type"
        ].create(
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

        cls.sold_property, cls.offered_property = cls.env["estate.property"].create(
            [
                {
                    "name": "sold_property",
                    "expected_price": 10_000,
                    "living_area": 100,
                    "property_type_id": cls.type_house.id,
                    "state": "sold",
                },
                {
                    "name": "offered_property",
                    "expected_price": 10_000,
                    "living_area": 100,
                    "property_type_id": cls.type_castle.id,
                    "state": "new",
                },
            ]
        )

        cls.env.flush_all()

    @tagged("post_install")
    def test_cannot_create_offer_on_sold_property(self):
        """Test that we cannot create an offer on property that is sold"""

        with self.assertRaises(ValidationError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "price": 10_000,
                        "partner_id": self.dummy_user.id,
                        "property_id": self.sold_property.id,
                    }
                ]
            )

    @tagged("post_install")
    def test_cannot_sell_property_with_no_accepted_offers(self):
        """Test that we cannot sell a property that has no accepted offers"""

        self.env["estate.property.offer"].create(
            [
                {
                    "price": 10_000,
                    "partner_id": self.dummy_user.id,
                    "property_id": self.offered_property.id,
                }
            ]
        )

        self.assertEqual(
            self.offered_property.state,
            "offer_received",
            "Adding offer to property did not change state to 'offer_received'",
        )

        with self.assertRaises(ValidationError):
            self.offered_property.sold_property()

    @tagged("post_install")
    def test_garden_onchange_works(self):
        """Test that the garden onchange works in the Form view for properties"""
        form = Form(self.sold_property)
        self.assertTrue(
            form._get_modifier("garden_area", "invisible"),
            "garden area should be invisible",
        )
        form.garden = True
        self.assertEqual(form.garden_area, 10)
        self.assertEqual(form.garden_orientation, "north")
