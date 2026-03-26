from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError


class EstatePropertyCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstatePropertyCommon, cls).setUpClass()

        cls.property = cls.env['estate.property'].create({'name': "Test Property",'expected_price': 1.0})

    def test_01_prevent_offer_for_sold_property(self):
        """Test that creating an offer for a sold property raises a UserError."""

        offer = self.env['estate.property.offer'].create({'property_id': self.property.id,'price': 2.0})
        offer.action_accept()

        self.property.action_sell()

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({'property_id': self.property.id,'price': 3.0})

    def test_02_prevent_sell_no_accepted_offers(self):
        """Test that selling a property without an accepted offer raises a UserError."""

        self.property.state = 'new'

        with self.assertRaises(UserError):
            self.property.action_sell()
