from odoo.exceptions import UserError
from odoo.tests import Form
from . import common


class EstateTest(common.EstatePropertyTestCommon):

    def test_sell_property(self):
            """Test that only properties with offers can be sold"""

            # Fail before any offer has been made
            with self.assertRaises(UserError):
                self.base_property.action_sell_property()

            self.env['estate.property.offer'].create({
                'price': 95_000,
                'property_id': self.base_property.id,
                'partner_id': self.env.company.partner_id.id
            }).action_accept_offer()

            self.assertTrue(self.base_property.action_sell_property())
            self.assertEqual(self.base_property.state, 'sold')

    def test_garden_checkbox_onchange(self):
        with Form(self.base_property) as account_form:
            account_form.garden = True
            
            self.assertEqual(account_form.garden_area, 10)
            self.assertEqual(account_form.garden_orientation, 'north')
