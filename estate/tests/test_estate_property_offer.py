from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstatePropertyOfferTestCase, cls).setUpClass()
        cls.property = cls.env['estate.property'].create({
                                                            'name': 'Test',
                                                            'expected_price': '1',
                                                            })

    def test_create_offer_for_cancelled(self):
        """Test that an offer cannot be created for a cancelled property."""
        self.property.state = 'cancelled'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': 1,
                'price': 1,
            })

    def test_create_offer_for_sold(self):
        """Test that an offer cannot be created for a sold property."""
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': 1,
                'price': 1,
            })
