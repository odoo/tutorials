from odoo.tests.common import TransactionCase


class EstateTestCommon(TransactionCase): 

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create([
            {"name": "Test 0", "status": "new", "expected_price": 100000, "garden_area": 0},
            {"name": "Test 1", "status": "new", "expected_price": 100000, "garden_area": 10},
            {"name": "Test 2", "status": "new", "expected_price": 100000, "garden_area": 50},
        ])
