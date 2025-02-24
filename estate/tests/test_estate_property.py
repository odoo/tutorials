from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()
        # Create a sample property with expected price and garden details.
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'state': 'new',
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'north',
            'expected_price': 100100,
        })

    def test_create_offer_on_sold_property(self):
        # Set the property state to sold.
        self.property.write({'state': 'sold'})
        # Attempting to create an offer on a sold property should raise a UserError.
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 100000,
                'partner_id': 2,
            })

    def test_sell_property_with_no_accepted_offer(self):
        # Create an offer that is not accepted (status remains 'refused').
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 100000,
            'partner_id': 2,
        })
        # Attempting to sell without an accepted offer should raise a UserError.
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_sell_property_with_accepted_offer(self):
        # Create an offer.
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 100000,
            'partner_id': 2,
        })
        # Confirm the offer which sets its status to 'accepted' and sets the property's selling price.
        offer.action_confirm()
        # Set the buyer for the property.
        self.property.write({'buyer_id': 2})
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')
        self.assertEqual(self.property.selling_price, 100000)

    def test_garden_reset_on_change(self):
        # Use the Form helper to simulate a form view, which triggers onchange events.
        with Form(self.property) as form:
            form.garden = False
        # Assert that the related fields have been reset
        self.assertFalse(self.property.garden_area,
                         "Garden Area should be reset when Garden is unchecked.")
        self.assertFalse(self.property.garden_orientation,
                         "Orientation should be reset when Garden is unchecked.")
