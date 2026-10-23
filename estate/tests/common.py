from odoo import Command
from odoo.tests import TransactionCase


class EstateTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_a = cls.env["estate.property"].create(
            {
                "name": "property_a",
                "expected_price": 100_000.00,
                "offer_ids": [
                    Command.create(
                        {"price": 98_000.00, "partner_id": cls.env.user.partner_id.id},
                    ),
                ],
            },
        )
