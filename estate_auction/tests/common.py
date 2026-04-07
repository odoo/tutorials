from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class EstateAuctionCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.email = "salesperson@example.com"
        cls.partner_a = cls.env["res.partner"].create({
            "name": "Auction Buyer A",
            "email": "buyer_a@example.com",
        })
        cls.partner_b = cls.env["res.partner"].create({
            "name": "Auction Buyer B",
            "email": "buyer_b@example.com",
        })

    def _create_property(self, **values):
        sale_type = values.pop("sale_type", "auction")
        property_values = {
            "name": "Testing Property",
            "expected_price": 100.0,
            "sale_type": sale_type,
        }
        if sale_type == "auction":
            property_values["auction_end_time"] = fields.Datetime.to_string(
                fields.Datetime.now() + timedelta(hours=1),
            )
        property_values.update(values)
        return self.env["estate.property"].create(property_values)

    def _create_offer(self, property_record, partner, price):
        return self.env["estate.property.offer"].create(
            {
                "property_id": property_record.id,
                "partner_id": partner.id,
                "price": price,
            },
        )
