from odoo.exceptions import UserError
from odoo.tests import tagged
from . import common


@tagged('post_install', '-at_install', 'estate_test')
class TestEstateOfferCreate(common.TestEstatePropertyCommon):
    @classmethod
    def setUpClass(cls):
        super(TestEstateOfferCreate, cls).setUpClass()

    def test_when_sold_status_should_not_create_offers(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create(
                {
                    'property_id': self.property_2.id,
                    'partner_id': self.contact_1.id,
                    'price': 9,
                }
            )
