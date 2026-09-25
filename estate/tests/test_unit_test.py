
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        estate_property_vals = {
            "name": "Sunny Villa near the Park",
            "description": "Spacious 3-bedroom villa with a bright living room, renovated kitchen and a quiet garden.",
            "postcode": "1000",
            "date_availability": date.today() - relativedelta(months=3),
            "expected_price": 350000.0,
            "bedrooms": 3,
            "living_area": 120,
            "facades": 3,
            "has_garage": True,
            "has_garden": True,
            "garden_area": 250,
            "garden_orientation": "south",
            "state": "new",
            "active": True,
            "buyer_id": False,
            "salesperson_id": 0,
            "offers_ids": [
                (0, 0, {"price": 340000.0, "partner_id": 0}),
                (0, 0, {"price": 355000.0, "partner_id": 0}),
            ],                             # One2many command: create related offers
        }
        estate_property_bis_vals = {
            "name": "une cacahuète de compétition",
            "description": "Probably shouldn't be on a real estate website",
            "postcode": "5020",
            "date_availability": date.today() - relativedelta(months=3),
            "expected_price": 35.0,
            "bedrooms": 3,
            "living_area": 120,
            "facades": 3,
            "has_garage": True,
            "has_garden": True,
            "garden_area": 250,
            "garden_orientation": "south",
            "state": "new",
            "active": True,
            "buyer_id": False,
            "salesperson_id": 0,
            "offers_ids": [
                (0, 0, {"price": 34.0, "partner_id": 0}),
                (0, 0, {"price": 35.5, "partner_id": 0}),
            ],                             # One2many command: create related offers
        }
        cls.properties = cls.env['estate_property'].create([estate_property_vals, estate_property_bis_vals])

    def test_estates_exist(self):
        self.assertEqual(len(self.properties), 2)

    def test_estates_sale(self):
        self.properties[0].state = 'offer_received'
        self.properties[0].offers_ids[0].action_accept_offer()
        self.properties[0].action_sell_property()

        self.assertRecordValues(self.properties, [{'state': 'sold'}, {'state': 'offer_received'}])
