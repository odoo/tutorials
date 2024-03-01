from odoo.addons.estate.tests.common import EstateTestCommon
from odoo.exceptions import UserError


class TestCreateOffer(EstateTestCommon):

    def test_create_offer(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 120,
                'partner_id': self.partner_1.id,
                'property_id': self.property_2.id
            })
