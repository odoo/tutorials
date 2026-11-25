from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.buyer = cls.env['res.partner'].create({
            "name": "test Buyer"
        })

        cls.properties = cls.env["estate.property"].create([
            {
                "name": "Big Villa",
                "expected_price": 1000000,
                "living_area": 100,
                "garden": True,
                "garden_area": 50,
            },
            {
                "name": "Small Apartment",
                "expected_price": 200000,
                "living_area": 40,
                "garden": False,
            },
        ])

    def _sell_properties(self, properties):
        """Helper to create offers, accept them, and mark properties as sold."""
        offers = self.env["estate.property.offer"].create([
            {
                "price": prop.expected_price,
                "partner_id": self.buyer.id,
                "property_id": prop.id,
            }
            for prop in properties
        ])
        offers.action_accept_offer()
        properties.action_set_sold()

    def test_sell_without_accepted_offer(self):
        """Test that a property without accepted offer cannot be sold."""
        with self.assertRaises(UserError):
            self.properties[0].action_set_sold()

        self.env["estate.property.offer"].create({
            "price": 1000000,
            "partner_id": self.buyer.id,
            "property_id": self.properties[0].id
        })

        with self.assertRaises(UserError):
            self.properties[0].action_set_sold()

    def test_action_sell(self):
        """test that a property can be sold once it has an accepted offer."""
        self._sell_properties(self.properties)
        self.assertRecordValues(self.properties, [
            {"name": "Big Villa", "state": "sold"},
            {"name": "Small Apartment", "state": "sold"},
        ])

    def test_cancel_sold_property(self):
        """Test that a sold property cannot then be cancelled"""
        self._sell_properties(self.properties)
        with self.assertRaises(UserError):
            self.properties.action_set_cancelled()

    def test_create_offer_on_sold_property(self):
        """Test that creating an offer on a sold property raises an error."""
        self._sell_properties(self.properties)

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create({
                "price": 2000000,
                "partner_id": self.buyer.id,
                "property_id": self.properties[0].id
            })
