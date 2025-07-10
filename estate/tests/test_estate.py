from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.test_property_type = cls.env['estate.property.type'].create({
            'name': 'apartment'
        })

        cls.test_property_tag = cls.env['estate.property.tag'].create({
            'name': 'MetroCity'
        })

        cls.test_property = cls.env['estate.property'].create({
            'name': 'Karsandas Bungalow',
            'description': 'Huge Bungalow',
            'property_type_id': cls.test_property_type.id,
            'tag_ids': [(6,0,[cls.test_property_tag.id])],
            'expected_price': 500000,
            'garden': True,
            'garden_area': 100,
            'garden_orientation': 'north'
        })

        cls.test_property_offer = cls.env['estate.property.offer'].create({
            'price': 40000,
            'partner_id': 2,
            'property_id': cls.test_property.id
        })

    def test_create_property(self):
        """Test property creation"""
        property = self.env['estate.property'].create({
            'name': 'Another Test Property',
            'description': 'Another test property description',
            'expected_price': 1,
            'property_type_id': self.test_property_type.id
        })
        self.assertEqual(property.name, 'Another Test Property')
        self.assertEqual(property.property_type_id.name, 'apartment')

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.test_property.living_area = 20
        self.test_property.garden_area = 20
        self.assertRecordValues(self.test_property, [
           {'name': 'Karsandas Bungalow', 'total_area': 40},
        ])

    def test_create_offer_on_sold(self):
        """Test that offer is created after property sold raises error."""
        self.test_property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.test_property.id,
                'price': 105000,
            })

    def test_sell_property_with_no_accepted_offer(self):
        """Test that property is not being sold without accepting offer."""
        with self.assertRaises(UserError):
            self.test_property.action_sold()

    def test_breaking_reset_garden(self):
        """Test that onchange only apply to form views."""
        with Form(self.test_property) as f:
            f.garden = False
        self.assertEqual(self.test_property.garden_area, 0)
        self.assertEqual(self.test_property.garden_orientation, False)
