from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('at_install')
class EstateOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate_classic.property'].create({
            "name": "Cool House",
            "state": 'new',
            "expected_price": 100000,
        })

    def test_offer_not_on_sold_property(self):
        self.offer = self.env['estate_classic.property.offer'].create({
            "property_id": self.property.id,
            "partner_id": self.env['res.partner'].create({
                'name': 'partner_a',
            }).id,
        })
        self.property.offer_ids = [self.offer.id]
        self.offer.action_accept_offer()
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.offer = self.env['estate_classic.property.offer'].create({
                "property_id": self.property.id,
                "partner_id": self.env['res.partner'].create({
                    'name': 'partner_a',
                }).id,
            })
