from odoo import api
from odoo.exceptions import UserError
from odoo.tests import TransactionCase
from odoo.tests import Form


class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.property_type = cls.env['estate.property.type'].create({
            'name': 'Test Property Type'
        })
        cls.properties = cls.env['estate.property'].create({
            'name': 'Test Property 1',
            'property_type_id': cls.property_type.id,
            'expected_price': 100000,
        })

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'name': 'Test Property 1', 'total_area': 20}
        ])

    def test_creation_area_with_garden(self):
        """Test that the total_area is computed like it should when a garden is present."""
        self.properties.living_area = 20
        self.properties.garden = True
        self.properties.garden_area = 10
        self.assertRecordValues(self.properties, [
           {'name': 'Test Property 1', 'total_area': 30}
        ])

    def test_action_sell_without_buyer(self):
        """Test that selling a property without a buyer raises an error."""
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_action_cannot_offer_when_property_is_sold(self):
        """Test that a sold property cannot be offered."""
        self.properties.state = 'sold'

        offer = Form(self.env['estate.property.offer'])
        offer.price = 100000
        offer.partner_id = self.env['res.partner'].create({'name': 'Test Partner'})
        offer.property_id = self.properties
        with self.assertRaises(UserError):
            offer.save()

    def test_action_sold_property_is_marked_as_sold(self):
        """Test that selling a property marks it as sold."""
        partner = self.env['res.partner'].create({'name': 'Test Buyer'})

        # Ensure the offer price is >= 90% of expected_price so validation passes
        offer = self.env['estate.property.offer'].create({
            'price': self.properties.expected_price,
            'partner_id': partner.id,
            'property_id': self.properties.id,
        })

        # Accept the offer (in the Odoo estate module, this sets buyer_id & selling_price)
        offer.action_accept_offer()

        # Trigger the "Mark as Sold" button action
        self.properties.action_sold()

        # Verify the property state and related fields
        self.assertEqual(self.properties.state, 'sold')
        self.assertEqual(self.properties.buyer_id, partner)
        self.assertEqual(self.properties.selling_price, self.properties.expected_price)
