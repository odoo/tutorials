from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEstatePropertyOffer(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.buyer = cls.env['res.partner'].create({'name': 'buyer'})

    def test_good_offer(self):
        self.property = self.env['estate.property'].create({
            'name': 'property1',
            'expected_price': 100,
        })
        offer = self.env['estate.property.offer'].create({
            'price': 90,
            'partner_id': self.buyer.id,
            'property_id': self.property.id,
        })
        self.assertRecordValues(self.property.offer_ids, [
            {'price': 90, 'partner_id': self.buyer.id}
        ])
        self.assertEqual(self.property.state, "offer")

    def test_offer_for_sold(self):
        self.property = self.env['estate.property'].create({
            'name': 'property1',
            'expected_price': 100,
            'state': 'sold'
        })
        with self.assertRaises(UserError):
            offer = self.env['estate.property.offer'].create({
                'price': 90,
                'partner_id': self.buyer.id,
                'property_id': self.property.id,
            })
        self.assertFalse(self.property.offer_ids, "after failure there should be no offer added")
        self.assertEqual(self.property.state, "sold", "after failure the state should not change")
