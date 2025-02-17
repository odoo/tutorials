from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError,ValidationError
from odoo.tests import tagged,Form
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase,cls).setUpClass()
        print()
        print()
        print("TEST FILE HAS BEEN INITIALIZED!!!!")
        print()
        print()

        cls.properties = cls.env['estate.property'].create({
            'name':'Test Property',
            'description':"test property",
            'postcode':'12345',
            'date_availability':'2024-12-31',
            'expected_price':150000.0,
            'state':'new',
            'garden':True
        })
        cls.offer1 = cls.env['estate.property.offer'].create({
            'price':140000.0,
            'property_id':cls.properties.id,
            'partner_id':2
        })
        cls.properties2 = cls.env['estate.property'].create({
            'name':'Test Property2',
            'description':"test property2",
            'postcode':'12345',
            'date_availability':'2024-12-31',
            'expected_price':150000.0,
            'state':'offer accepted'
        })

    def test_offer_create_after_sold(self):
        print("---------------------------Test1-----------------------------------------")
        print()
        self.properties2.sold()
        print("CREATING OFFER FOR SOLD PROPERTY!!!!")
        print()
        print()
        print(self.assertRaises(ValidationError))
        with self.assertRaises(ValidationError):
            self.env['estate.property.offer'].create({
                'property_id':self.properties2.id,
                'price':210000.0
            })
        print("Offer for sold property test Complete!")
       
    def test_no_sold_without_accept_offer(self):
        print("------------------Test2-------------------------------------")
        print()
        print("SELLING PROPERTY")
        with self.assertRaises(UserError):
            self.properties.sold()

        print("Selling property without accepting offer test completed!")    

    def test_garden_toggle_check(self):
        print()
        print()
        print("-------------------------------------------------TEST3--------------------------------")
        with Form(self.properties) as form:
            form.garden = False
            self.assertEqual(form.garden_area, 0, "Garden Area should be reset to 0 when Garden checkbox is unchecked")
            self.assertEqual(form.garden_orientation, False, "Garden Orientation should be reset to False when Garden checkbox is unchecked")
        print("3rd TEST CLEARED!!!!!!")