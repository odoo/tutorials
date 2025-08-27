from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError,ValidationError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name':'test1',
            'expected_price': 2,
            'garden_area':100
        })
        cls.offer = cls.env['estate.property.offer'].create({
            'price':100,
            'partner_id': cls.env.ref('base.res_partner_1').id,
            'property_id': cls.property.id
        })

    def test_cannot_create_offer(self):
        self.property.status="sold"
        with self.assertRaises(
            UserError, msg="Cannot create offer for sold property"
        ):
            self.env['estate.property.offer'].create({
                'price': 100,
                'partner_id':self.env.ref('base.res_partner_1').id,
                'property_id': self.property.id
            })

    def test_sell_property_no_offers(self):
        with self.assertRaises(
            UserError, msg="Cannot sold property because no offer is accepted"
        ):
            self.property.action_sold()
