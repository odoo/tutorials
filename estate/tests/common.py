from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_type = cls.env["estate.property.type"].create(
            {
                "name": "Residential",
            },
        )

        cls.property_tag = cls.env["estate.property.tag"].create(
            {
                "name": "Cozy",
            },
        )

        cls.buyer = cls.env["res.partner"].create(
            {
                "name": "John Doe",
            },
        )

        cls.salesman = cls.env["res.users"].create(
            {
                "name": "Jane Smith",
                "login": "jane_smith",
                "email": "jane.smith@example.com",
            },
        )

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Initial House",
                "description": "A very cozy house",
                "postcode": "12345",
                "expected_price": 100000.0,
                "bedrooms": 3,
                "living_area": 100,
                "facades": 4,
                "garage": True,
                "garden": True,
                "garden_area": 50,
                "garden_orientation": "north",
                "property_type_id": cls.property_type.id,
                "tag_ids": [Command.link(cls.property_tag.id)],
                "salesman_id": cls.salesman.id,
            },
        )
