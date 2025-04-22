from .test_common import EstateTestCommon
from odoo.exceptions import UserError


class TestEstatePropertyOffer(EstateTestCommon):

    def test_cannot_sell_property_without_accepted_offer(self):
        """Ensure a property cannot be sold without an accepted offer."""
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_sell_property_with_accepted_offer(self):
        # Create a partner for the offer
        partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 200000,
            'status': 'accepted',
            'partner_id': partner.id,
        })
        self.property.buyer_id = partner.id
        self.property.action_set_sold()
        self.assertEqual(self.property.status, 'sold', "Property should be marked as sold.")
