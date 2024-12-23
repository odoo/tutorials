
from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase

@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create([
            {
                "name": "Standard Appartment",
                "description": "A cozy appartment in the center of Liège",
                "postcode": "4000",
                "state": "new",
                "expected_price": 800000
            }
        ])

        cls.property_with_offers = cls.env["estate.property"].create([
            {
                "name": "4 Side House",
                "description": "A luxury house in Beaufays",
                "postcode": "4052",
                "expected_price": 1200000,
                "state": "new",
                "offer_ids": [
                    Command.create({
                        "price": 1150000,
                        "status": "accepted",
                        "partner_id": 1
                    })
                ]
            }
        ])

    def test_cannot_sell_property_when_no_offers(self):
        self.assertRecordValues(self.properties, [
            {
                "name": "Standard Appartment",
                "description": "A cozy appartment in the center of Liège",
                "postcode": "4000",
                "state": "new",
                "expected_price": 800000
            }
        ])

        with self.assertRaises(UserError):
            self.properties.action_set_state_sold()
            self.fail("Should have failed")
    
    def test_can_sell_property_if_accepted_offer(self):
        self.assertRecordValues(self.property_with_offers, [
            {
                "name": "4 Side House",
                "description": "A luxury house in Beaufays",
                "postcode": "4052",
                "expected_price": 1200000,
                "state": "received", 
            }
        ])

        self.assertRecordValues(self.property_with_offers.offer_ids, [
                    {
                        "price": 1150000,
                        "status": "accepted",
                        "partner_id": 1
                    }
                ]
        )

        self.property_with_offers.action_set_state_sold()

        self.assertRecordValues(self.property_with_offers, [
            {
                "name": "4 Side House",
                "description": "A luxury house in Beaufays",
                "postcode": "4052",
                "expected_price": 1200000,
                "state": "sold" 
            }
        ])

    def test_cannot_create_offer_for_sold_property(self):
        with self.assertRaises(UserError):
            self.env["estate.property"].create([
                {
                    "name": "4 Side House",
                    "description": "A luxury house in Beaufays",
                    "postcode": "4052",
                    "expected_price": 1200000,
                    "state": "sold",
                    "offer_ids": [
                        Command.create({
                            "price": 1150000,
                            "status": "accepted",
                            "partner_id": 1
                        })
                    ]
                }
            ])
            self.fail("Should have failed")

    def test_garden_resets_when_unchecked(self):
        estate_form = Form(self.env["estate.property"])

        estate_form.garden = True
        self.assertEqual(10, estate_form.garden_area)
        self.assertEqual("north", estate_form.garden_orientation)

        estate_form.garden = False
        self.assertEqual(0, estate_form.garden_area)
        self.assertEqual(False, estate_form.garden_orientation)
