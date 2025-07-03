from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form


class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def test_forbidden_action_on_sold_property(self):
        property = self.env["estate.property"].create(
            {
                "name": "City Apartment",
                "expected_price": 17500,
            }
        )

        self.env["estate.property.offer"].create(
            {
                "price": 150000.00,
                "partner_id": self.env.ref("base.res_partner_1").id,
                "deadline": "2025-09-14",
                "property_id": property.id,
                "status": "accepted",
            }
        )

        property.action_sold()

        with self.assertRaises(
            UserError, msg="Cannot create an offer for a sold property"
        ):
            self.env["estate.property.offer"].create(
                {
                    "price": 150000000.00,
                    "partner_id": self.env.ref("base.res_partner_1").id,
                    "deadline": "2025-09-14",
                    "property_id": property.id,
                }
            )


def test_no_accept_offer(self):
    property = self.env["estate.property"].create(
        {
            "name": "City Apartment2",
            "expected_price": 16500,
        }
    )

    self.env["estate.property.offer"].create(
        {
            "price": 150000.00,
            "partner_id": self.env.ref("base.res_partner_1").id,
            "deadline": "2025-09-14",
            "property_id": property.id,
        }
    )

    with self.assertRaises(UserError, msg="Can not sold without accept offer"):
        property.action_sold()


def test_reset_garden_area_and_orientation(self):
    property = self.env["estate.property"].create(
        {
            "name": "TEST PROPERTY",
            "expected_price": "1334",
            "garden": True,
            "garden_area": 50,
            "garden_orientation": "north",
        }
    )

    with Form(property) as form:
        form.garden = False
        form.save()

    self.assertFalse(property.garden, "The garden checkbox is not selected..")
    self.assertFalse(
        property.garden_area,
        "Garden area should be reset when garden checkbox is not selected.",
    )
    self.assertFalse(
        property.garden_orientation,
        "Orientation should be reset when garden checkbox is not selected.",
    )
