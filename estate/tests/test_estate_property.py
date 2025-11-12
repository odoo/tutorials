from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Setup test data before each test."""
        super().setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 1000000,
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'west',
        })
        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Test Buyer'
        })
        
    def test_cannot_create_offer_on_sold_property(self):
        """Test that an offer cannot be created for a sold property."""
        self.property.write({'state': 'sold'})

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.partner_a.id,
                'price': 6000000
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        """Test that a property cannot be sold if no offer has been accepted."""
        with self.assertRaises(UserError):
            self.property.action_set_property_sold()

    def test_can_sell_property_with_accepted_offer(self):
        """Test that a property is correctly marked as sold after selling."""
        self.offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 5000000,
            'partner_id': self.partner_a.id
        })


        self.offer.action_accept()  # Accept the offer
        self.property.action_set_property_sold()

        self.assertEqual(self.property.state, 'sold', "Property should be marked as sold.")

    def test_garden_field_onchange_behavior(self):
        """Test that unchecking 'garden' does not incorrectly reset 'garden_area' and 'garden_orientation'."""
        form = Form(self.property)
        
        # Ensure initial values
        self.assertTrue(form.garden)
        self.assertEqual(form.garden_area, 50)
        self.assertEqual(form.garden_orientation, 'west')

        # Uncheck 'garden'
        form.garden = False
        form.save()

        self.assertEqual(self.property.garden, False)
        self.assertEqual(self.property.garden_area, 0, "Garden area should be 0.")
        self.assertEqual(self.property.garden_orientation, False, "Garden orientation should be False('').")

        # Re-check 'garden' and ensure values stay the same
        form.garden = True
        form.save()
        
        self.assertEqual(self.property.garden, True)
        self.assertEqual(self.property.garden_area, 10, "Garden area should 10.")
        self.assertEqual(self.property.garden_orientation, 'north', "Garden orientation should be set to north")

    def test_cannot_accept_offer_below_90_percent_selling_price(self):
        """Test that an offer cannot be accepted if the price is less than 90% of expected price."""
        low_price = self.property.expected_price * 0.90 - 1
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_a.id,
            'price': low_price
        })

        with self.assertRaises(UserError):
            offer.action_accept()

    def test_can_accept_offer_above_90_percent_selling_price(self):
        """Test that an offer can be accepted if the price is more than 90% of expected price."""
        valid_price = self.property.expected_price * 0.90 + 1  # Just above 90%
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.partner_a.id,
            'price': valid_price
        })

        offer.action_accept()  # Accept the offer

        self.assertEqual(
            self.property.selling_price,
            valid_price,
            "Property selling price should be updated after accepting the offer."
        )
        self.assertEqual(
            self.property.state,
            'offer_accepted',
            "Property state should be updated to 'offer_accepted' after accepting the offer."
        )
