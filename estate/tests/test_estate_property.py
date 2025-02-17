from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, Form, TransactionCase

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(self):
        super(EstateTestCase, self).setUpClass()
        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        self.properties = self.env['estate.property'].create([
            {'name': 'Property 1','state': 'new', 'expected_price': 10}
        ])

        self.offer1 = self.env['estate.property.offer'].create([{
            'property_id':self.properties.id,
            'partner_id':14,
            'price' : 1000,
            'status' :"accepted"
        }])
  
    # def test_sell_a_property_with_no_accepted_offers(self):
    #     with self.assertRaises(UserError):
    #         self.properties.action_sold()

    def test_create_offer_for_a_sold_property(self):
        print("-------------------------------1------------------------------------------")
        self.properties.state="sold"
        with self.assertRaises(UserError):
                    self.env['estate.property.offer'].create([{
                        'property_id':self.properties.id,
                        'partner_id' : 14,
                        'price':20000,
                    }])
    def test_sell_a_property_with_no_accepted_offers(self):
        print("------------------------------2-----------------------------------------")
        self.offer1.status='refused'
        with self.assertRaises(UserError):
            self.properties.action_sold()

    def test_sold_is_correctly_marked(self):
        self.offer1.action_confirm()
        self.properties.action_sold()
        self.assertEqual(self.properties.state,"sold","Property Should be marked as sold after selling it.")

    def test_uncheck_check_garden_checkbox(self):
        estate_form = Form(self.properties)
        
        estate_form.garden= False
        self.assertEqual(estate_form.garden_orientation,False)
        self.assertEqual(estate_form.garden_area, 0)
        print(estate_form.garden_area)
        print(estate_form.garden_orientation)
        print("UNcheck funtion")

        estate_form.garden= True
        self.assertEqual(estate_form.garden_orientation,"north")
        self.assertEqual(estate_form.garden_area, 10)
        print(estate_form.garden_area)
        print(estate_form.garden_orientation)
        print("check funtion")
