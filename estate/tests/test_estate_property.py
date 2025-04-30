from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Jack",
        })

        cls.property = cls.env["estate_property"].create({
            "name": "TestingHouse",
            "expected_price": 250000,
            "description": "House created for testing",
        })

    def test_sell_without_offer(self):
        with self.assertRaises(UserError):
            self.property.mark_as_sold()

    def test_create_offer_with_lower_best_price(self):
        #define best price
        self.env["estate_property_offer"].create({
            "price": 250000,
            "partner_id": self.partner.id,
            "property_id": self.property.id,
            "date_deadline": fields.Datetime.today()
        })
        #try to create offer less than 90% of the best price
        with self.assertRaises(UserError):
            self.env["estate_property_offer"].create({
                "price": 20,
                "partner_id": self.partner.id,
                "property_id": self.property.id,
                "date_deadline": fields.Datetime.today()
            })

    def test_create_offer_for_sold_property(self):
        offer = self.env["estate_property_offer"].create({
            "price": 250000,
            "partner_id": self.partner.id,
            "property_id": self.property.id,
            "date_deadline": fields.Datetime.today()
        })
        offer.action_confirm()
        with self.assertRaises(UserError):
            self.env["estate_property_offer"].create({
                        "price": 250000,
                        "partner_id": self.partner.id,
                        "property_id": self.property.id,
                        "date_deadline": fields.Datetime.today()
                    })
