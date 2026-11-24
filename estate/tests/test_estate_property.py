from odoo.tests import TransactionCase
from odoo.exceptions import UserError


class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create({"name": "Test Buyer"})
        cls.properties = cls.env["estate.property"].create([
            {"name": "house1", "expected_price": 1}
        ])
        cls.offers = cls.env["estate.property.offer"].create([
            {"price": 1, "property_id": cls.properties.id, "partner_id": cls.partner.id}
        ])

    def test_unlink_sold(self):
        """Test that a sold property can't be deleted."""

        self.offers.action_do_accept()
        self.properties.action_do_sell()
        self.assertRecordValues(self.properties, [{"state": "sold"}])

        with self.assertRaises(UserError):
            self.properties.unlink()

    def test_unlink_accepted(self):
        """Test that a property with an accepted offer can't be deleted."""

        self.offers.action_do_accept()
        self.assertRecordValues(self.properties, [{"state": "offer_accepted"}])

        with self.assertRaises(UserError):
            self.properties.unlink()

    def test_creation_offer_when_sold(self):
        """Test that an offer can't be created when the property is already sold."""

        self.offers.action_do_accept()
        self.properties.action_do_sell()

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create({
                "property_id": self.properties.id
            })

    def test_sell_no_accepted_offers(self):
        """Test that a property with no accepted offer can't be sold."""

        with self.assertRaises(UserError):
            self.properties.action_do_sell()
