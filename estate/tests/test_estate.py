from odoo.fields import Properties
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        
        demo_properties =[
            {
                "name": "property_1",
                "state": "new",
                "expected_price": 100000.0,
                "living_area": 100,
                "garden": True,
                "garden_area": 100,
            },
            {
                "name": "property_2",
                "state": "offer_accepted",
                "expected_price": 102000.0,
                "living_area": 1000,
                "garden": True,
                "garden_area": 100,
                "garden_orientation": "south"
            },
            {
                "name": "property_3",
                "state": "cancelled",
                "expected_price": 1600000.0,
                "living_area": 100
            }
        ]
        cls.properties = cls.env['estate.property'].create(demo_properties)
        
        demo_offers = [
            {
                'property_id': cls.properties[0].id,
                'partner_id': cls.env.ref('base.res_partner_1').id,
                'price': 96000
            },
            {
                'property_id': cls.properties[0].id,
                'partner_id': cls.env.ref('base.res_partner_2').id,
                'price': 95000
            }
        ]
        cls.offers = cls.env['estate.property.offer'].create(demo_offers)


    # Test that the total_area is computed like it should
    def test_compute_total_area(self):
        self.assertRecordValues(self.properties, [
           {'name': 'property_1', 'total_area': 200},
           {'name': 'property_2', 'total_area': 1100},
           {'name': 'property_3', 'total_area': 100}
        ])


    # Test that the onchange_garden is computed like it should
    def test_onchange_garden(self):
        for property in self.properties:
            with Form(property) as form:
                form.garden = True
                self.assertEqual(form.garden_area, 10)
                self.assertEqual(form.garden_orientation, "north")
                form.garden = False
                self.assertEqual(form.garden_area, 0)
                self.assertEqual(form.garden_orientation, False) 


    # Testing action_sold() with different type of property state
    def test_action_sold(self):
        for property in self.properties:

            # test for property in cancelled state
            if property.state == 'cancelled':
                with self.assertRaises(UserError, msg="Cancelled properties cannot be sold"):
                    property.action_sold()

            # test for property not in offer accepted state
            elif property.state != 'offer_accepted':
                with self.assertRaises(UserError, msg="Property cannot be sold without an offer accepted"):
                    property.action_sold()

            # test for property in sold state
            else:
                property.action_sold()
                self.assertEqual(property.state, 'sold', "Property state should change to 'sold'")


    # Testing action_cancel() with different type of property state
    def test_action_cancel(self):
        for property in self.properties:

            # test for property in sold state
            if property.state == 'sold':
                with self.assertRaises(UserError, msg="Sold properties cannot be cancelled"):
                    property.action_cancel()

            # test for property not in cancelled state
            else:
                property.action_cancel()
                self.assertEqual(property.state, 'cancelled', "Property state should change to 'cancalled'")


    # Testing unlink() with different type of property state
    def test_unlink(self):
        for property in self.properties:

            # test for property not in new or and cancelled state
            if not property.state in ['new', 'cancelled']:
                with self.assertRaises(UserError, msg="Only new or cancelled state properties can be deleted"):
                    property.unlink()

            # test for property in new or cancelled state
            else:
                property.unlink()
                self.assertFalse(property.exists(), "Property should be deleted")


    # Testing ction_accept() with accepting different offers to the same property
    def test_action_accept(self):

        # Attempt to accept the first offer
        self.offers[0].action_accept()
        self.assertEqual(self.offers[0].state, 'accepted', "First offer should be accepted")
        self.assertEqual(self.properties[0].state, 'offer_accepted', "Property state should change to 'offer_accepted'")
        self.assertEqual(self.properties[0].buyer_id, self.offers[0].partner_id, "Property buyer should be set to the offer's partner")
        self.assertEqual(self.properties[0].selling_price, self.offers[0].price, "Property selling price should be set to the offer's price")

        # Attempt to accept the second offer
        with self.assertRaises(UserError, msg="An Offer is already been accepted"):
            self.offers[1].action_accept()

        self.assertEqual(self.offers[0].state, 'accepted', "Fisrt offer should be accepted")
        self.assertNotEqual(self.offers[1].state, 'accepted', "Second offer should not be accepted")

    # Testing ction_refuse() with refusing different offers to the same property
    def test_action_refuse(self):
        self.offers[0].action_refuse()
        self.assertEqual(self.offers[0].state, 'refused', "offer should be refused")
