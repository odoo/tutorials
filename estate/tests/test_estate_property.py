from odoo import Command
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_type = cls.env['estate.property.type'].create({
            'name': 'VillaTest',
        })

        cls.property_tag = cls.env['estate.property.tag'].create({
            'name': 'Modern',
            'color': 1,
        })

        cls.buyers = cls.env['res.partner'].create({
            'name': 'John Doe',
        })

        cls.property = cls.env['estate.property'].create({
            'name': 'Villa Bahamas',
            'expected_price': 200000,
            'property_type_id': cls.property_type.id,
            'tag_ids': [cls.property_tag.id],
        })

    def test_create_and_accept_offer(self):
        offers = self.env['estate.property.offer'].create([
            {
                'price': 180000,
                'partner_id': self.buyers.id,
                'validity': 10,
                'property_id': self.property.id,
            },
            {
                'price': 190000,
                'partner_id': self.buyers.id,
                'validity': 10,
                'property_id': self.property.id,
            },
        ])

        self.assertEqual(
            len(self.property.offer_ids),
            2,
            '2 offers should be attached to the property',
        )

        offers[1].action_accept()

        self.assertEqual(
            self.property.state,
            'offer_accepted',
            'Property state should be offer_accepted',
        )
        self.assertEqual(
            offers[1].status,
            'accepted',
            'Offer status should be accepted',
        )
        self.assertEqual(
            self.property.selling_price,
            offers[1].price,
            'Selling price should match the accepted offer price',
        )
        self.assertEqual(
            self.property.buyer,
            self.buyers,
            'Property buyer should match the offer partner',
        )
