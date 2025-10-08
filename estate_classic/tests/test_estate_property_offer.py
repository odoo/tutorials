from odoo.exceptions import UserError
from . import test_estate_property


class EstateOfferTestCase(test_estate_property.EstateTestCase):

    def test_offer_not_on_sold_property(self):
        self.offer = self.env['estate_classic.property.offer'].create({
            "property_id": self.property.id,
            "partner_id": self.partner_a.id,
            "price": 105000,
        })
        self.offer.action_accept_offer()
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.offer = self.env['estate_classic.property.offer'].create({
                "property_id": self.property.id,
                "partner_id": self.partner_a.id,
                "price": 105000,
            })
