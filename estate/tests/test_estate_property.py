from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestEstateProperty, cls).setUpClass()
        cls.property = cls.env[estate.property].create({
            'name' : 'Test Property',
            'living_area' : 1000,
            'garden' : True,
            'garden_area' : 10,
            'garden_orientation' : 'east',
            'total_area' : 1010,
            'state' : 'new',
            'expected_price' : 10000
        })
        cls.offer_accepted = cls.env['estate.property.offer'].create({
            'property_id': cls.property.id,
            'price': 12000,
            'status': 'accepted'
        })


    def test_create_offer_for_sold_property(self):
        #Test that you cannot create an offer for a sold property
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 11000,
                'status': 'draft'
            })

    def test_sell_property_without_accepted_offer(self):
        #Test that you cannot sell a property with no accepted offers
        self.property.state, self.property.offer_ids = 'new', []
        with self.assertRaises(UserError):
            self.property.action_sold() 

    def test_sell_property_with_accepted_offer(self):
        #Test that a property with an accepted offer can be sold and marked as sold
        self.property.offer_ids = [(4, self.new_offer.id, {'state': 'offer_received'})]
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold')

    def test_garden_area_and_garden_orientation_on_garden_check(self) :
        #Test that in a property garden area and garden orientation is reset when garden's checkbox is unchecked (garden = False)
        self.property.garden = False
        self.property._onchange_garden()
        self.assertEqual(self.garden_area, 0)
        self.asserFalse(self.garden_orientation)
