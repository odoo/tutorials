from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form


class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env['estate.property']

    def test_creation_offer(self):
        property = self.properties.create({
            'name': 'Test Property',
            'expected_price': 1000,
            'garden': True,
            'garden_area': 20,
            'garden_orientation': 'south',
            'state': 'sold',
        })

        with self.assertRaises(
                UserError, msg="Cannot create an offer for a sold property"
        ):
            self.env["estate.property.offer"].create(
                {
                    "price": 1500.00,
                    "partner_id": self.env.ref("base.res_partner_1").id,
                    "date_deadline": "2025-09-14",
                    "property_id": property.id,
                }
            )

    def test_sold_property(self):
        property = self.properties.create({
            'name': 'Test Property Demo',
            'expected_price': 100,
            'garden': True,
            'garden_area': 20,
            'garden_orientation': 'south',
            'state': 'new',
        })

        self.env['estate.property.offer'].create({
            'property_id': property.id,
            'partner_id': self.env.ref('base.res_partner_2').id,
            "validity": 7,
            'price': 1200,
        })

        with self.assertRaises(UserError):
            property.action_sold()

    def test_reset_garden_area_and_orientation(self):
        property = self.env["estate.property"].create(
            {
                "name": "Garden Test Property",
                "expected_price": "789",
                "garden": True,
                "garden_area": 50,
                "garden_orientation": "north",
            }
        )

        with Form(property) as form:
            form.garden = False
            form.save()

        self.assertFalse(property.garden, "Garden checkbox should be unchecked.")
        self.assertFalse(
            property.garden_area,
            "Garden area should be reset when the garden checkbox is unchecked.",
        )
        self.assertFalse(
            property.garden_orientation,
            "Orientation should be reset when the garden checkbox is unchecked.",
        )
