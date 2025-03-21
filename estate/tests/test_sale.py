#type:ignore
from .test_common import EstateTestCommon
from odoo.exceptions import UserError


class TestEstatePropertySale(EstateTestCommon):

    def test_cannot_create_offer_for_sold_property(self):
        """Ensure an offer cannot be created for a sold property."""
        self.property.status = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 100000,
                'partner_id': self.partner.id,
            })
