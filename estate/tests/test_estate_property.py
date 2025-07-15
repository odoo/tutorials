from odoo.tests.common import TransactionCase, Form
from odoo.tests import tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test properties
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'garden': True,
            'garden_area': 50,
            'garden_orientation': 'north',
            'state': 'new'
        })

        cls.sold_property = cls.env['estate.property'].create({
            'name': 'Sold Property',
            'state': 'sold'
        })

        cls.offer_property = cls.env['estate.property'].create({
            'name': 'Offer Property',
            'state': 'offer_accepted'
        })

        cls.accepted_offer = cls.env['estate.property.offer'].create({
            'property_id': cls.offer_property.id,
            'price': 100000,
            'status': 'accepted'
        })

    def test_reset_garden_fields(self):
        """Test that unchecking the garden resets garden_area and garden_orientation."""
        form = Form(property)
        form.garden = False  # Unchecking garden checkbox
        form.save()

        self.assertEqual(self.property.garden_area, 0, "Garden Area should be reset to 0")
        self.assertFalse(self.property.garden_orientation, "Garden Orientation should be reset to False")

    def test_prevent_offer_on_sold_property(self):
        """Test that a user cannot create an offer on a sold property."""
        with self.assertRaises(UserError, msg="Cannot create offer for a sold property"):
            self.env['estate.property.offer'].create({
                'property_id': self.sold_property.id,
                'price': 50000
            })

    def test_prevent_selling_without_accepted_offer(self):
        """Test that a property cannot be sold if no offer is accepted."""
        with self.assertRaises(UserError, msg="Cannot sell property without an accepted offer"):
            self.property.action_sold()

    def test_successful_property_sale(self):
        """Test that a property with an accepted offer can be sold."""
        self.offer_property.action_sold()
        self.assertEqual(self.offer_property.state, 'sold', "Property should be marked as sold")
