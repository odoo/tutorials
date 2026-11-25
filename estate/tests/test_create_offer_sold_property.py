from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class CreateOfferSoldPropertyCase(TransactionCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()

        self.partner = self.env['res.partner'].create({
            'name': "Partner test person"
        })
        self.property = self.env['estate.property'].create({
            'name': "Awesome property for testing",
            'expected_price': 200_000,
            'state': "new"
        })
        self.offer = self.env['estate.property.offer'].create({
            'price': 200_000,
            'state': "accepted",
            'partner_id': self.partner.id,
            'property_id': self.property.id
        })
        self.property.action_sell_property()

    def test_create_offer_sold_property(self):
        with self.assertRaises(UserError):
            # New offer that we will try to add to the property
            self.env['estate.property.offer'].create({
                'price': 222_000,
                'partner_id': self.partner.id,
                'property_id': self.property.id
            })
