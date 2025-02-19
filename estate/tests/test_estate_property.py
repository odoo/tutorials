from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged,Form,TransactionCase

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()
        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.property = cls.env['estate.property'].create([
            {'name': 'Property 1','status': 'new', 'expected_price': 10}
        ])

        cls.partner_id = cls.env['res.partner'].create({'name': 'Demo Partner'})

        cls.offer1 = cls.env['estate.property.offer'].create([{
            'property_id':cls.property.id,
            'partner_id':cls.partner_id.id,
            'price' : 1000,
            'status_offer' :"accepted"
        }])
  
    # def test_sell_a_property_with_no_accepted_offers(cls):
    #     with cls.assertRaises(UserError):
    #         cls.property.action_sold()

    def test_create_offer_for_a_sold_property(cls):
        print("-------------------------------1------------------------------------------")
        cls.property.status="sold"
        with cls.assertRaises(UserError):
                    cls.env['estate.property.offer'].create([{
                        'property_id':cls.property.id,
                        'partner_id' : cls.partner_id.id,   #change
                        'price':20000,
                    }])
    def test_sell_a_property_with_no_accepted_offers(cls):
        print("------------------------------2-----------------------------------------")
        cls.offer1.status_offer='refused'
        with cls.assertRaises(UserError):
            cls.property.sold_event()

    def test_sold_is_correctly_marked(cls):
        print("------------------------------3-----------------------------------------")
        print(cls.property.status)
        cls.offer1.accept_offer()
        print(cls.property.status)
        cls.property.sold_event()
        cls.assertEqual(cls.property.status,"sold","Property Should be marked as sold after selling it")
 
    def test_garden_onchange_reset_and_resotre(cls):
        print("------------------------------4-----------------------------------------")
        estate_form=Form(cls.property)
        estate_form.garden=True
        cls.assertEqual(estate_form.garden_area,1000)
        cls.assertEqual(estate_form.garden_orientation,"north")
        print("CHECK TEST CASE IS PASSED!")
        print(estate_form.garden_area," ",estate_form.garden_orientation)
        estate_form.garden=False
        cls.assertEqual(estate_form.garden_area,0)
        cls.assertEqual(estate_form.garden_orientation,False)
        print("==="*50)
        print("UNCHECK TEST CASE IS PASSED!")
        print(estate_form.garden_area," ",estate_form.garden_orientation)

