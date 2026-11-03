from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create({'name': 'TestPartnes'})

        cls.emptyProperty = cls.env['estate.property'].create({'name': 'testHouse', 'expected_price': 10})
        cls.normalProperty = cls.env['estate.property'].create({'name': 'testHouse', 'expected_price': 10})

        cls.offer1 = cls.env['estate.property.offer'].create({"partner_id": cls.partner, "property_id": cls.normalProperty, "price": 20})

    def test_on_creation_sell(self):
        """Test that properties can't be sold if they are newly created"""
        with self.assertRaises(UserError):
            self.emptyProperty.sell_property()
        self.assertRecordValues(self.emptyProperty, [{'state': 'new'}])

    def test_offer_for_sold_property(self):
        self.normalProperty.sell_property()
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({"partner_id": self.partner, "property_id": self.normalProperty, "price": 2000})
