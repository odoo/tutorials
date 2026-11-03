from odoo import Command, fields
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        property_type = cls.env['estate_property_type'].create({
            'name': 'House',
            'description': 'A test property type',
        })
        tag = cls.env['estate_property_tag'].create({
            'name': 'Test Tag',
            'description': 'A test property tag',
            'color': 1,
        })
        buyer = cls.env['res.partner'].create({
            'name': 'Test Buyer',
        })
        cls.properties = cls.env['estate_property'].create([{
            'name': 'Test Property',
            'description': 'A fully configured test property',
            'postcode': '12345',
            'date_availability': fields.Date.add(fields.Date.today(), months=2),
            'expected_price': 100000,
            'selling_price': 95000,
            'bedrooms': 3,
            'living_area': 100,
            'facades': 2,
            'garage': True,
            'garden': True,
            'garden_area': 20,
            'garden_orientation': 'north',
            'state': 'sold',
            'property_type_id': property_type.id,
            'salesman_id': cls.env.user.id,
            'buyer_id': buyer.id,
            'tag_ids': [Command.set([tag.id])],
            'active': True,
            'sequence': 1,
        }])

    def test_creation_sold_offers(self):
        """Test that you cannot create an offer on a sold property."""
        self.assertRecordValues(self.properties, [
            {'name': 'Test Property', 'state': 'sold'},
        ])
        self.assertRaises(ValidationError, lambda: self.env['estate_property_offer'].create({
            'price': 95000,
            'partner_id': self.properties.buyer_id.id,
            'property_id': self.properties.id,
            'validity': 7,
            'status': None,
            'active': True,
            'sequence': 1,
        }))
