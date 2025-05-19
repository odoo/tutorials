from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestEstate(TransactionCase):
    def setUp(self):
        super(TestEstate, self).setUp()
        self.property = self.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
        })
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})

    def test_no_offer_on_sold_property(self):
        """Test that an offer cannot be created for a sold property."""
        self.property.status = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 95000,
                'partner_id': self.partner.id,
            })

    def test_no_sell_without_accepted_offer(self):
        """Test that a property cannot be sold without an accepted offer."""
        with self.assertRaises(UserError):
            self.property.sold_property()

    def test_sell_with_accepted_offer(self):
        """Test that a property is correctly marked as sold when it has an accepted offer."""
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'price': 95000,
            'partner_id': self.partner.id,
        })
        self.property.selling_price=95000
        offer.status = 'accepted'
        self.property.sold_property()
        self.assertEqual(self.property.status, 'sold')
