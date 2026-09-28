from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.buyers = cls.env['res.partner'].create({
            'name': 'Jerome Verkyndt',
        })

        cls.property = cls.env['estate.property'].create({
            'name': 'House Test',
            'description': 'des test test',
            'postcode': '5081',
            'expected_price': 250000.0,
            'bedrooms': 4,
            'living_area': 100,
            'facades': 4,
            'garage': True,
            'garden': True,
            'garden_area': 100,
            'garden_orientation': 'north',
            'state': 'new',
        })

    def test_valid_offer(self):

        offer_1 = self.env["estate.property.offer"].create({
                'price': 1000000,
                'partner_id': self.buyers.id,
                'validity': 7,
                'property_id': self.property.id
            })
        offer_2 = self.env["estate.property.offer"].create({
                'price': 2000000,
                'partner_id': self.buyers.id,
                'validity': 7,
                'property_id': self.property.id
            })

        self.assertRecordValues(
            self.property, [{"offer_ids": {offer_1.id, offer_2.id}}]
        )

        offer_2.action_set_accepted()


        self.assertRecordValues(offer_2, [{"status": "accepted"}])
        self.assertRecordValues(offer_1, [{"status": "refused"}])
