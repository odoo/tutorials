from odoo.exceptions import UserError
from . import common



class EstatePropertyOfferTest(common.EstatePropertyTestCommon):

    def test_create_offer_for_property(self):
            """Test that creating a new offer for a property works as expected.
                If the property is sold or cancelled it should fail
                Otherwise, should be possible
            """
            self.env['estate.property.offer'].create({
                'price': 90_000,
                'property_id': self.base_property.id,
                'partner_id': self.env.company.partner_id.id
            }).action_accept_offer()

            self.base_property.action_sell_property()

            with self.assertRaises(UserError):
                self.env['estate.property.offer'].create({
                    'price': 95_000,
                    'property_id': self.base_property.id,
                    'partner_id': self.env.company.partner_id.id
                })
