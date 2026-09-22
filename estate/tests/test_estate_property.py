from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """Create a single property"""
        cls.property = cls.env['estate.property'].create(
            [{
                'name': 'House on the beach',
                'expected_price': 100000,
                'postcode': 5000,
                'state': 'new'
            }])

    def test_sell_property(self):
        """
        Try to sell the property without any accepted offer
        This should raise an UserError
        """
        with self.assertRaises(UserError):
            self.property.action_sell_property_state()

        """
        Add and accept an offer on the property
        Then sell the property
        """
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': partner.id,
            'price': 100000,
        })
        offer.action_accept_property_offer()
        self.property.action_sell_property_state()
        # Check that the state of the property changed to "sold"
        self.assertEqual(self.property.state, 'sold')

    def test_garden_info_reset(self):
        """
        Enable the garden in the property
        This should set the value of:
        - garden_area to 10
        - garden_orientation to "North"
        """
        # Create the "form view" server side
        with Form(self.property) as f1:
            f1.has_garden = True
            self.assertEqual(f1.garden_area, 10)
            self.assertEqual(f1.garden_orientation, 'north')
            # Change the garden_area & orientation
            f1.garden_area = 100
            f1.garden_orientation = 'south'
            self.assertEqual(f1.garden_area, 100)
            self.assertEqual(f1.garden_orientation, 'south')
            # Reset the has_garden variable (Simulate uncheck and re-check the box)
            f1.has_garden = False
            self.assertEqual(f1.garden_area, 0)
            self.assertEqual(f1.garden_orientation, False)
            # Re-check has_garden
            f1.has_garden = True
            """
            The property value should be:
            - garden_area to 10
            - garden_orientation to "North"
            """
            self.assertEqual(f1.garden_area, 10)
            self.assertEqual(f1.garden_orientation, 'north')
