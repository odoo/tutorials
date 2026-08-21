from odoo.addons.base.tests.common import BaseCommon


class EstatePropertyCommon(BaseCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.estate_property_types = cls.env["estate.property.type"].create([
            {"name": "House"},
            {"name": "Apartment"},
        ])
        cls.estate_property_tags = cls.env["estate.property.tag"].create([
            {"name": "tag1"},
            {"name": "tag2"},
        ])
        cls.estate_properties = cls.env["estate.property"].create([
            {
                "name": "Property 1",
                "expected_price": 100.0,
            },
            {
                "name": "Property 2",
                "expected_price": 150.0,
            },
        ])
