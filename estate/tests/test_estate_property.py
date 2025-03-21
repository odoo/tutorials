from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    def setUp(self):
        super(TestEstateProperty, self).setUp()
        self.property = self.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'status': 'new',
            'garden': True,
        })
        self.offer = self.env['estate.property.offer'].create({
            'price': 1000000,
            'property_id': self.property.id,
            'partner_id': self.env.ref('base.res_partner_12').id
        })

    def test_cannot_create_offer_for_sold_property(self):
        self.property.status = 'sold'
        with self.assertRaises(UserError, msg="You cannot create an offer for a sold property."):
            self.env['estate.property.offer'].create({
                'price': 800000,
                'property_id': self.property.id,
                'partner_id': self.env.ref('base.res_partner_12').id
            })

    def test_cannot_sell_property_with_no_accepted_offers(self):
        with self.assertRaises(UserError, msg="Accept an offer first."):
            self.property.action_sold()

    def test_can_sell_property_with_accepted_offer(self):
        self.offer.action_accept()
        self.property.action_sold()
        
        self.assertEqual(self.property.status, 'sold')

    def test_onchange_garden(self):
        form = Form(self.property)
        form.garden = False

        self.assertEqual(form.garden_area, 0)
        self.assertEqual(form.garden_orientation, False)