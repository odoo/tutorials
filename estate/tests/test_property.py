from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError, ValidationError
# from odoo.tests import tagged


# @tagged('post_install', '-at_install')
class TestProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestProperty, cls).setUpClass()

        # Create property once for all tests
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'garden': True,
            'garden_area': 50,
            'orientation': 'north',
        })

        # Create buyer once
        cls.buyer = cls.env['res.partner'].create({'name': 'Test Buyer'})

        # Create offer once
        cls.offer = cls.env['estate.property.offer'].create({
            'property_id': cls.property.id,
            'partner_id': cls.buyer.id,
            'price': 95000,
        })

    def test_offer_on_sold_property(self):
        """ Test that an offer cannot be created for a sold property """
        self.property.state = 'sold'

        with self.assertRaises(UserError):
            self.offer.action_accept()

    def test_successful_property_sale(self):
        """ Test that a property with an accepted offer can be sold """
        self.offer.action_accept()
        self.property.action_sold()

        self.assertEqual(self.property.state, 'sold')
        self.assertEqual(self.property.buyer_id, self.buyer)
        self.assertEqual(self.property.selling_price, self.offer.price)

    def test_garden_uncheck_reset(self):
        """Ensure garden_area and orientation reset when garden is unchecked."""

        with Form(self.property) as form:
            # Ensure initial values are correctly set
            self.assertTrue(form.garden)
            self.assertEqual(form.garden_area, 50)
            self.assertEqual(form.orientation, 'north')

            # Uncheck the Garden field
            form.garden = False
            form.save()

        # Refresh the record to get updated values from the database
        self.property.invalidate_recordset()

        # Check if garden is unchecked
        self.assertFalse(self.property.garden, "Garden should be unchecked.")

        # Check if the garden_area and orientation are reset correctly
        self.assertEqual(self.property.garden_area, 0, "Garden area should reset to 0.")
        self.assertFalse(self.property.orientation, "Orientation should reset to False or empty.")
