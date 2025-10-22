from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env['estate.property'].create({"name": "Test house", "expected_price": 240000})
        cls.partner = cls.env['res.partner'].create({"name": "Partner"})

    def test_offer_creation(self):
        """Test that the offer cannot be created if the property is sold."""
        self.env['estate.property.offer'].create({"price": 240000, "partner_id": self.partner.id, "property_id": self.properties.id, 'status': 'accepted'})
        self.properties.state = 'sold'

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({"price": 240000, "partner_id": self.partner.id, "property_id": self.properties.id})
