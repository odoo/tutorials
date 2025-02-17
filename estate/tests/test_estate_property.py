from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        partner = cls.env['res.partner'].create({'name': 'Test Buyer'})

        # print('----------------------Add Property------------------------')
        cls.properties = cls.env['estate.property'].create([
            {'name':'Property p1',
            'expected_price':1500,
            'state':'new',
            'buyer_id':partner.id}
        ])
        cls.properties_offer = cls.env['estate.property.offer'].create({
                'price': 1530,
                'partner_id': partner.id,  
                'property_id': cls.properties.id,  
            })

    def test_create_offer_on_sold_property(self):
        # print('----------------------Test case 1------------------------')
        self.properties_offer.action_accept_offer()
        partner = self.env['res.partner'].create({'name': 'Test Buyer'})

        # Mark property as sold
        self.properties.action_set_sold()

        # Attempt to create an offer on a sold property - should raise UserError
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 1600,
                'validity': 14,
                'partner_id': partner.id,  
                'property_id': self.properties.id, 
            })


    def test_sell_property_without_accepted_offer(self):
        """Test that a property cannot be sold without an accepted offer."""
        # print('----------------------Test case 2------------------------')

        with self.assertRaises(UserError):
            self.properties.action_set_sold()

    def test_selling_property(self):
        """Test that selling a property correctly updates its state."""
        # print('----------------------Test case 3------------------------')
        partner = self.env['res.partner'].create({'name': 'Test Buyer'})

        offer = self.env['estate.property.offer'].create({
            'price': 1600,
            'property_id': self.properties.id,
            'partner_id': partner.id,
        })
        offer.status = 'accepted' 
        self.properties.action_set_sold()
        self.assertEqual(self.properties.state, 'sold')

def test_garden_checkbox(self):
    # Test when garden checkbox is unchecked
    with Form(self.properties) as property:
        property.garden = False
        self.assertEqual(property.garden_orientation, False)
        self.assertEqual(property.garden_area, 0)

    # Test when garden checkbox is checked
    with Form(self.properties) as property:
        property.garden = True
        self.assertEqual(property.garden_orientation, 'north')
        self.assertEqual(property.garden_area, 20)
