from odoo import fields
from odoo.tests import TransactionCase


class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.record = cls.env["estate.property"].create(
                        {
                            "name": "test_name",
                            "description": "test_description",
                            "postcode": "1234",
                            "expected_price": 10000.00,
                            "bedrooms": 2,
                            "living_area": 10,
                            "facades": 4,
                            "has_garage": True,
                            "has_garden": True,
                            "garden_area": 5,
                            "garden_orientation": "north",
                        },
                    )
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.property_id = cls.record.id

        cls.offer1_record = cls.env["estate.property.offer"].create(
                            {
                                "partner_id": cls.partner.id,
                                "property_id": cls.property_id,
                                "price": 9000.00,
                            },
                        )

        cls.offer2_record = cls.env["estate.property.offer"].create(
                            {
                                "partner_id": cls.partner.id,
                                "property_id": cls.property_id,
                                "price": 10000.00,
                            },
                        )

    def test_create_property(self):
        """
        Test if property is properly created
        Test if offer are properly created, comfirmed and refused
        """

        # Check basic Fields
        self.assertRecordValues(
            self.record,
            [
                {
                    "name": "test_name",
                    "description": "test_description",
                    "postcode": "1234",
                    "expected_price": 10000.00,
                    "bedrooms": 2,
                    "living_area": 10,
                    "facades": 4,
                    "has_garage": True,
                    "has_garden": True,
                    "garden_area": 5,
                    "garden_orientation": "north",
                },
            ],
        )

        # Check Default and Computed Fields
        self.assertEqual(self.record.total_area, 10 + 5)
        self.assertEqual(
            self.record.date_availability,
            fields.Date.add(fields.Date.today(), months=3),
        )
        self.assertEqual(self.record.selling_price, 0)
        self.assertEqual(self.record.best_price, 10000.00)
        self.assertEqual(self.record.active, True)

        self.assertEqual(len(self.record.offer_ids), 2)
        self.assertIn(self.offer1_record, self.record.offer_ids)
        self.assertIn(self.offer2_record, self.record.offer_ids)

        # Confirm Offer
        self.offer2_record.action_confirm_offer()

        self.assertEqual(self.offer2_record.status, "accepted")
        # Check Compute Field of Property
        self.assertEqual(self.record.selling_price, 10000.00)

        # Refuse Offer
        self.offer1_record.action_refuse_offer()

        self.assertEqual(self.offer1_record.status, "refused")
