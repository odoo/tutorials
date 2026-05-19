from odoo.exceptions import UserError
from odoo.tests import Form, new_test_user, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "estate")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env["estate.property"].create(
            [{"name": "Farm 1", "expected_price": 1_000_000}]
        )

    def test_creation_area(self):
        """Test that the total_area is properly computed."""
        self.properties.living_area = 200
        self.properties.garden_area = 100
        self.assertRecordValues(
            self.properties, [{"name": "Farm 1", "total_area": 300}]
        )

    def test_garden_area_and_orientation(self):
        # when garden is True
        with Form(self.env["estate.property"]) as property:
            property.name = "Farm 2"
            property.expected_price = 2_000_000
            property.garden = True

        # then garden_area and garden_orientation are set
        self.assertRecordValues(
            property.record, [{"garden_area": 10, "garden_orientation": "north"}]
        )

        # when garden is False
        property.garden = False
        property.save()

        # garden_area and garden_orientation are disabled
        self.assertRecordValues(
            property.record, [{"garden_area": 0, "garden_orientation": False}]
        )

    def test_no_offer_allowed_for_sold_properties(self):
        # when property is sold
        self.properties.state = "sold"
        buyer = new_test_user(self.env, login="mark_baier@example.com")

        # then new offer cannot be made
        with self.assertRaises(UserError):
            self.properties.offer_ids = self.env["estate.property.offer"].create(
                [
                    {
                        "property_id": self.properties.id,
                        "price": 1_000_000,
                        "partner_id": buyer.partner_id.id,
                    }
                ]
            )

    def test_properties_cannot_be_sold_without_accepted_offer(self):
        # when property has no offer it cannot be marked sold
        with self.assertRaises(UserError):
            self.properties.action_mark_sold_property()

        # when property has no accepted offer it cannot be marked sold
        buyer = new_test_user(self.env, login="mark_baier@example.com")
        offer = self.env["estate.property.offer"].create(
            [
                {
                    "property_id": self.properties.id,
                    "price": 1_000_000,
                    "partner_id": buyer.partner_id.id,
                }
            ]
        )
        with self.assertRaises(UserError):
            self.properties.action_mark_sold_property()

        # when property has an accepted offer it can be marked sold
        offer.action_accept()
        self.properties.action_mark_sold_property()

        self.assertRecordValues(self.properties, [{"state": "sold"}])
