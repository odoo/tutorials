from odoo.tests.common import TransactionCase
from odoo.tests import tagged, Form
from odoo.exceptions import UserError


@tagged("post_install", "-at_install")
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_type = cls.env["estate.property.type"].create(
            {"name": "House Test Type"}
        )

        cls.properties = cls.env["estate.property"].create(
            [
                {
                    "name": "Sale Test Property",
                    "description": "Test Description",
                    "expected_price": 100000,
                    "living_area": 50,
                    "property_type_id": cls.property_type.id,
                },
                {
                    "name": "Garden Test Property",
                    "description": "Test Description Garden",
                    "expected_price": 200000,
                    "living_area": 100,
                    "property_type_id": cls.property_type.id,
                },
            ]
        )

        cls.offers = cls.env["estate.property.offer"].create(
            [
                {
                    "partner_id": cls.env.ref("base.res_partner_2").id,
                    "price": 110000,
                    "property_id": cls.properties[0].id,
                    "validity": 7,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_12").id,
                    "price": 130000,
                    "property_id": cls.properties[0].id,
                    "validity": 7,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_2").id,
                    "price": 150000,
                    "property_id": cls.properties[0].id,
                    "validity": 7,
                },
            ]
        )

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.properties[0].action_sell_property()

    def test_sold_property_cannot_create_offer(self):
        self.properties[0].write({"state": "offer_accepted"})
        self.properties[0].action_sell_property()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                [
                    {
                        "partner_id": self.env.ref("base.res_partner_2").id,
                        "price": 110000,
                        "property_id": self.properties[0].id,
                        "validity": 7,
                    },
                ]
            )

    def test_garden_toggle(self):
        with Form(self.properties[1]) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10, "Garden area should be reset to 10")
            self.assertEqual(
                form.garden_orientation,
                "north",
                "Garden orientation should be reset to north",
            )
            form.garden = False
            self.assertEqual(form.garden_area, 0, "Garden area should be reset to 0")
            self.assertEqual(
                form.garden_orientation,
                False,
                "Garden orientation should be reset to False",
            )
