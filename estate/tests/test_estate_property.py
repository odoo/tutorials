from odoo.tests.common import TransactionCase, tagged
from odoo.tests import Form
from odoo.exceptions import UserError

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 400000,
            'garden': True,
            'garden_area': 400,
            'garden_orientation': 'west',
        })
        cls.offer = cls.env['estate.property.offer'].create({
            'price': 1000000,
            'property_id': cls.property.id,
            'partner_id': cls.env.ref('base.res_partner_12').id
        })

    def test_prevent_offer_on_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError, msg="Cannot create an offer for a sold property."):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': self.env.ref('base.res_partner_12').id,
                'price': 6000000
            })

    def test_prevent_selling_property_without_accepted_offer(self):
        """Test that a property cannot be sold without an accepted offer."""
        with self.assertRaises(UserError, msg="You cannot sell a property without an accepted offer."):
            self.property.button_sold_action()

    def test_selling_property_with_accepted_offer(self):
        """Test that a property with an accepted offer can be sold."""
        self.offer.status = 'accepted'
        self.property.button_sold_action()
        self.assertEqual(self.property.state, 'sold', "Property should be marked as sold.")

    def test_garden_reset(self):
        """Test that unchecking Garden resets Garden Area and Orientation."""
        with Form(self.property) as prop_form:
            prop_form.garden = False
        self.assertEqual(self.property.garden_area, 0, "Garden area should be reset to 0.")
        self.assertFalse(self.property.garden_orientation, "Orientation should be reset.")
