from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class EstatePropertyOfferTest(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstatePropertyOfferTest, cls).setUpClass()

        # Create a property
        cls.property = cls.env["estate.property"].create(
            {
                "name": "Luxury Hut with sandy water",
                "description": "A beautiful hut in the city center",
                "postcode": "12345",
                "expected_price": 500000,
                "status": "new",  # Default state
            }
        )

        cls.offers = cls.env["estate.property.offer"].create(
            {
                "price": 600000,
                "partner_id": cls.env.ref("base.res_partner_12").id,
                "property_id": cls.property.id,
            }
        )

    def test_cannot_create_offer_for_sold_property(self):
        """Ensure that an offer cannot be made on a sold property."""
        # Change the property state to 'sold'
        self.property.status = "sold"

        # Attempt to create an offer
        with self.assertRaises(
            UserError, msg="Offer cant be created for a sold property"
        ):
            self.env["estate.property.offer"].create(
                {
                    "price": 600000,
                    "property_id": self.property.id,
                    "partner_id": self.env.ref("base.res_partner_12").id,
                }
            )

    def test_cannot_sell_property_with_no_accepted_offer(self):
        """Ensure that an property cannot be sold if there is no offer accepted"""
        with self.assertRaises(
            UserError, msg="Property cant be sold if there is no offer accept"
        ):
            self.property.action_estate_property_sold()
