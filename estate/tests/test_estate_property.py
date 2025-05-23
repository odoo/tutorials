from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import tagged, Form
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_type = cls.env["estate.property.type"].create({"name": "House Test Type"})

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
                    "offer_price": 110000,
                    "property_id": cls.properties[0].id,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_12").id,
                    "offer_price": 130000,
                    "property_id": cls.properties[0].id,
                },
                {
                    "partner_id": cls.env.ref("base.res_partner_2").id,
                    "offer_price": 150000,
                    "property_id": cls.properties[0].id,
                },
            ]
        )

    def test_sell_property_without_accepted_offer(self):
        """
        Test selling a property without an accepted offer.
        Ensure that a UserError is raised when trying to sell a property without an accepted offer.
        Ensure that other offers are not allowed to be created after the property is sold.
        """

        with self.assertRaises(UserError):
            self.properties[0].action_set_sold()

        self.offers[1].action_accept()
        self.properties[0].action_set_sold()

        self.assertEqual(
            self.properties[0].state, "sold", "Property was not marked as sold"
        )

        with self.assertRaises(UserError):
            self.properties[0].offer_ids = [
                Command.create(
                    {
                        "partner_id": self.env.ref("base.res_partner_2").id,
                        "price": 200000,
                        "property_id": self.properties[0].id,
                    }
                )
            ]

    def test_garden_toggle(self):
        """
        Test toggling the garden field on the property.
        Ensure that the garden area and orientation are resetting.
        """

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
