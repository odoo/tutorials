from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, Form

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
class EstatePropertyTestCase(TransactionCase):

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

        cls.properties_no_offers = cls.env['estate_property'].create([{
            'name': 'Test Property No Offers',
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
            'state': 'new',
            'property_type_id': property_type.id,
            'salesman_id': cls.env.user.id,
            'buyer_id': buyer.id,
            'tag_ids': [Command.set([tag.id])],
            'active': True,
            'sequence': 1,
        }])
        cls.properties_with_offer = cls.env['estate_property'].create([{
            'name': 'Test Property with Offer',
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
            'state': 'new',
            'property_type_id': property_type.id,
            'salesman_id': cls.env.user.id,
            'buyer_id': buyer.id,
            'tag_ids': [Command.set([tag.id])],
            'active': True,
            'sequence': 1,
        }])

        cls.offers = cls.env['estate_property_offer'].create([{
            'price': 95000,
            'partner_id': buyer.id,
            'property_id': cls.properties_with_offer.id,
            'validity': 7,
            'status': 'accepted',
            'active': True,
            'sequence': 1,
        }])

    def test_sell_property(self):
        """Test that you can sell a property correctly and it is marked as sold."""
        self.assertRecordValues(self.properties_with_offer, [
            {'name': 'Test Property with Offer', 'state': 'offer_received'},
        ])
        self.properties_with_offer.action_sold_estate_property()
        self.assertRecordValues(self.properties_with_offer, [
            {'name': 'Test Property with Offer', 'state': 'sold'},
        ])

    def test_sell_property_with_no_accepted_offer(self):
        """Test that you cannot sell a property with no accepted offers."""
        self.assertRecordValues(self.properties_no_offers, [
            {'name': 'Test Property No Offers', 'state': 'new'},
        ])
        with self.assertRaises(UserError):
            self.properties_no_offers.action_sold_estate_property()

        self.env['estate_property_offer'].create([{
            'price': 90000,
            'partner_id': self.properties_no_offers.buyer_id.id,
            'property_id': self.properties_no_offers.id,
            'validity': 7,
            'status': None,
            'active': True,
            'sequence': 2,
        }])
        with self.assertRaises(UserError):
            self.properties_no_offers.action_sold_estate_property()
        self.assertRecordValues(self.properties_no_offers, [
            {'name': 'Test Property No Offers', 'state': 'offer_received'},
        ])

    def test_garden_form(self):
        """Test that the garden form works correctly."""
        self.assertRecordValues(self.properties_no_offers, [
            {'name': 'Test Property No Offers', 'garden': True, 'garden_area': 20, 'garden_orientation': 'north'},
        ])
        f = Form(self.properties_no_offers)
        f.garden = False
        property_no_garden = f.save()
        self.assertRecordValues(property_no_garden, [
            {'name': 'Test Property No Offers', 'garden': False, 'garden_area': 0, 'garden_orientation': False},
        ])
