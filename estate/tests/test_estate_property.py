from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name': 'Property 1',
            'expected_price': 100000,
        })
        cls.buyer = cls.env['res.partner'].create({
            'name': 'Buyer',
        })

    def test_sold_no_offer(self):
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_sold_offer(self):
        offer = self.env['estate.property.offer'].create({
            'price': 100000,
            'partner_id': self.buyer.id,
            'property_id': self.property.id,
        })
        self.assertFalse(offer.status)
        self.assertTrue(self.property.offer_ids)
        self.assertEqual(len(self.property.offer_ids), 1)

        offer.action_validate()
        self.assertEqual(offer.status, 'accepted')
        self.assertEqual(self.property.state, 'offer_accepted')

        self.property.action_set_sold()
        self.assertEqual(self.property.state, 'sold')
        self.assertEqual(self.property.buyer, offer.partner_id)
        self.assertEqual(self.property.selling_price, offer.price)

        # Ensure that we can't create any offer on a sold property
        # Tested it here because we need to have a sold property
        # to test this constraint and we built one here
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 100000,
                'partner_id': self.buyer.id,
                'property_id': self.property.id,
            })

    def test_garden_area(self):
        property_form = Form(self.property)
        property_form.garden = True
        self.assertEqual(property_form.garden_orientation, 'north')
        self.assertEqual(property_form.garden_area, 10)
        self.property.garden = False
        self.assertFalse(self.property.garden_orientation)
        self.assertEqual(self.property.garden_area, 0)
