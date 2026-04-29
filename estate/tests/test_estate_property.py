from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.estate = cls.env['estate.property'].create({
            'name': 'Super test estate',
            'expected_price': 100000.0,
            'state': 'new',
        })
        cls.test_partner = cls.env['res.partner'].create({
            'name': 'Maman ours',
        })

    def test_estate_best_price(self):
        '''
        Ensure best price is correctly updated when an offer is received.
        '''
        self.assertEqual(self.estate.best_price, 0.0)
        self.estate.offer_ids = [Command.create({
            'price': 125000.0,
            'partner_id': self.test_partner.id,
        })]
        self.assertEqual(self.estate.best_price, 125000.0)

    def test_accept_offer_south_facing_garden(self):
        '''
        Ensure offers for estates with south-facing gardens can only be accepted if above expected
        price.
        '''
        self.estate.garden = True
        self.estate.garden_orientation = 'south'
        self.estate.expected_price = 500000
        self.estate.offer_ids = [Command.create({
            'price': 475000.0,
            'partner_id': self.test_partner.id,
        })]
        with self.assertRaises(ValidationError):
            self.estate.offer_ids.action_accept_offer()
