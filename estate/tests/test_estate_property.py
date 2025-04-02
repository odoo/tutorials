from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError

class PropertyTest(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(EstatePropertyTest, cls).setUpClass()

        properties = [{
            'name':'Big Villa',
            'state':'sold',
            'description':'A nice and big villa',
            'postcode':12345,
            'date_availability':'2024-04-04',
            'expected_price':1600000,
            'bedrooms':6,
            'living_area':100,
            'facades':4,
            'garage':True,
            'garden':True,
            'garden_area':100000,
            'garden_orientation':'south',
        },{
            'name':'Big Villa',
            'state':'sold',
            'description':'A nice and big villa',
            'postcode':12345,
            'date_availability':'2024-04-04',
            'expected_price':1600000,
            'bedrooms':6,
            'living_area':100,
            'facades':4,
            'garage':True,
            'garden':True,
            'garden_area':100000,
            'garden_orientation':'south',
        }]

        cls.property = cls.env['estate.property'].create(properties)

    def test_property_sell_with_no_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_offer_create_on_sold_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property[0].id,
                'partner_id': self.env.ref('base.res_partner_12').id,
                'price': 1600000
            })
