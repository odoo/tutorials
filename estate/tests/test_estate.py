from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form

@tagged('post_install', '-at_install')
class EstateTestClass(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestClass, cls).setUpClass()
        demo_properties =[
            {
                "name": "property_1",
                "state": "new",
                "expected_price": 500000.0,
                "living_area": 200,
                "garden": True,
                "garden_area": 100,
            },
            {
                "name": "property_2",
                "state": "offer_accepted",
                "expected_price": 10000000.0,
                "living_area": 800,
                "garden": True,
                "garden_area": 200,
                "garden_orientation": "south"
            },
            {
                "name": "property_3",
                "state": "cancelled",
                "expected_price": 500000.0,
                "living_area": 300
            }
        ]

        cls.properties = cls.env['estate.property'].create(demo_properties)

    def test_compute_total_area(self):
        """Test the total_area is computed correctly."""
        self.assertRecordValues(self.properties, [
           {'name': 'property_1', 'total_area': 300},
           {'name': 'property_2', 'total_area': 1000},
           {'name': 'property_3', 'total_area': 300}
        ])
        self.properties.living_area = 500 
        self.assertRecordValues(self.properties, [
           {'name': 'property_1', 'total_area': 600},
           {'name': 'property_2', 'total_area': 700},
           {'name': 'property_3', 'total_area': 500 }
        ])

    def test_onchange_garden(self):
        """Test the onchange_garden is computed like it should"""
        for property in self.properties:
            with Form(property) as form:
                form.garden = True
                self.assertEqual(form.garden_area, 10, 'Garden area default 10 when garden is eanble')
                self.assertEqual(form.garden_orientation, "north", 'Garden orientation default north when garden is eanble')
                form.garden = False
                self.assertEqual(form.garden_area, 0, 'Garden area 0 when garden is disable')
                self.assertEqual(form.garden_orientation, False, 'Garden orientation default false when garden is disable')

    def test_create_offer_on_sold_property(self):
        """Test the offer can receied by sold property"""
        self.properties[1].action_sold_button()
        with self.assertRaises(UserError, msg="Cannot create an offer for a sold property."):
            self.env['estate.property.offer'].create([{
                'property_id': self.properties[1].id,
                'partner_id': self.env.ref('base.res_partner_1').id,
                'price': 96000
            }])

    def test_sold_action_button(self):
        """Test the sold button for different state"""
        for property in self.properties:
            if property.state == 'cancelled':
                with self.assertRaises(UserError, msg="Cancelled property cannot be sold."):
                    property.action_sold_button()
            elif property.state != 'offer_accepted':
                with self.assertRaises(UserError, msg="Not an any offer has Accepted."):
                    property.action_sold_button()
            else:
                property.action_sold_button()
                self.assertEqual(property.state, 'sold', "Property state should change to 'sold'")
