from odoo.tests import TransactionCase
from odoo.tools import mute_logger


class EstatePropertyTagTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_type = cls.env['estate.property.type'].create({
            'name': 'Test Property Type'
        })
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property 1',
            'property_type_id': cls.property_type.id,
            'expected_price': 100000,
        })

    def test_tags_should_be_unique(self):
        self.env['estate.property.tag'].create({
            'name': 'Test Tag 1'
        })
        self.env['estate.property.tag'].create({
            'name': 'Test Tag 2'
        })
        with self.assertRaisesRegex(Exception, 'unique_name'), mute_logger('odoo.sql_db'):
            with self.cr.savepoint():
                self.env['estate.property.tag'].create({
                    'name': 'Test Tag 1'
                })

    def test_tags_color_can_be_whatever(self):
        """Color can be whatever. If someone adds a constraint on it in the future, this test will show that it was intentional"""
        tag1 = self.env['estate.property.tag'].create({
            'name': 'Test Tag 1'
        })
        tag2 = self.env['estate.property.tag'].create({
            'name': 'Test Tag 2'
        })
        tag1.color = 1
        tag2.color = 1
        tag1.color = 2
