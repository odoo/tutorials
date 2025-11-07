from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'state': 'new'
        })
        cls.offer = cls.env['estate.property.offer'].create({
            'price': 150000,
            'property_id': cls.property.id,
            'status': 'accepted'
        })

    def test_prevent_selling_without_accepted_offer(self):
        """Test that selling a property without an accepted offer is blocked."""
        property = self.env['estate.property'].create({'name': 'No Offer Property'})
        with self.assertRaises(UserError):
            property.action_sold()

    def test_prevent_offer_on_sold_property(self):
        """Test that an offer cannot be created for a sold property."""
        self.property.action_sold()
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({'price': 200000, 'property_id': self.property.id})

    def test_successful_property_sale(self):
        """Test that a property with an accepted offer can be sold."""
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold', "Property should be marked as sold.")

    def test_garden_reset(self):
        """Ensure garden area and orientation reset when unchecking the garden field."""
        property = self.env['estate.property'].create({
            'name': 'Garden Test Property',
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'north'
        })

        # Simulate unchecking the garden field in a form view
        with Form(property) as form:
            form.garden = False
        property = form.save()

        self.assertEqual(property.garden_area, 0, "Garden area should reset to 0 when garden is unchecked.")
        self.assertFalse(property.garden_orientation, "Garden orientation should reset when garden is unchecked.")
