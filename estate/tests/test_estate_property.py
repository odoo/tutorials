from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()

        cls.type_house = cls.env['estate.property.type'].create({'name': 'House'})
        cls.type_apartment = cls.env['estate.property.type'].create({'name': 'Apartment'})

        cls.tag_urgent = cls.env['estate.property.tag'].create({'name': 'Urgent'})

        cls.buyer = cls.env['res.partner'].create({'name': 'John Doe'})

        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Test House',
                'property_type_id': cls.type_house.id,
                'tag_ids': [(6, 0, [cls.tag_urgent.id])],
                'expected_price': 100000.0,
                'bedrooms': 3,
                'living_area': 150,
                'facades': 4,
                'garden': True,
                'garden_area': 20,
                'garden_orientation': 'north',
            }
        ])

    def test_compute_total_area(self):
        for property_record in self.properties:
            expected_total = property_record.living_area + property_record.garden_area
            self.assertEqual(
                property_record.total_area,
                expected_total,
                f"""Total area for {property_record.name} 
                should be {expected_total} but got {property_record.total_area}"""
            )
