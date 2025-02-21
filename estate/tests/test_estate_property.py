from odoo.tests.common import TransactionCase
from odoo.tests import tagged, Form
from odoo.exceptions import UserError


@tagged('post_install','-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env['estate.property'].create([
            {
                'name': "Villa Serenity",
                'expected_price': 2500000,
                'garden': True,
                'garden_orientation': "east",
                'living_area': 2000,
                'garden_area': 300
            },
            {
                'name': "Cozy Cottage",
                'expected_price': 850000,
                'state': 'offer_accepted',
                'garden': False,
                'living_area': 750,
            },
            {
                'name': "Modern Apartment",
                'expected_price': 1500000,
                'garden': False,
                'living_area': 1200,
            },
            {
                'name': "Luxury Mansion",
                'state': 'cancelled',
                'expected_price': 5000000,
                'garden': True,
                'garden_orientation': "south",
                'living_area': 5000,
                'garden_area': 800
            }
        ]

        )

        cls.offer1 = cls.env['estate.property.offer'].create([
            {
                'property_id': cls.properties[0].id,
                'partner_id': cls.env.ref('base.res_partner_1').id,
                'price': 2550000
            }
        ])
        cls.offer2 = cls.env['estate.property.offer'].create([
            {
                'property_id': cls.properties[0].id,
                'partner_id': cls.env.ref('base.res_partner_2').id,
                'price': 2600000
            }
        ])

    def test_creation_area(self):
        expected_total_values = []
        for prop in self.properties:
            expected_total_values.append({"id":prop.id, "total_area": prop.living_area + prop.garden_area })
        self.assertRecordValues(self.properties,expected_total_values)

    def test_form_garden(self):
        for prop in self.properties:
            with Form(prop) as propform:
                propform.garden = False
                self.assertEqual(propform.garden_area,0,"Garden area should be zero when garden is set to False")
                self.assertEqual(propform.garden_orientation,False,"Garden orientation should not be set when garden is set to False")

                propform.garden = True
                self.assertEqual(propform.garden_area,10,"Default garden area should be 10")
                self.assertEqual(propform.garden_orientation,"north","Default garden orientation should be North")

    def test_offer_accept_btn(self):
        self.offer1.action_offer_accept_btn()
        self.assertEqual(self.offer1.status,"accepted","Offer status should be accepted after accepting the offer")
        self.assertEqual(self.offer1.property_id.selling_price,self.offer1.price,"selling price should be same as accepted offer price")
        self.assertEqual(self.offer1.property_id.buyer,self.offer1.partner_id,"Buyer should be same as the partner in accepted offer")
        self.assertEqual(self.offer1.property_id.state,"offer_accepted","Property status should be offer accepted after accepting offer")

    def test_second_offer_accept(self):
        self.offer1.action_offer_accept_btn()
        with self.assertRaises(UserError,msg = "No other offer can be accept after accepting one offer"):
            self.offer2.action_offer_accept_btn()

    def test_offer_reject_btn(self):
        self.offer1.action_offer_reject_btn()
        self.assertEqual(self.offer1.status,"refused","Offer status should be refused after rejecting the offer")

    def test_property_sold_btn(self):
        for prop in self.properties:
            if prop.state == 'cancelled':
                with self.assertRaises(UserError,msg="Cancelled Property cant be sold"):
                    prop.action_sold_btn()
            elif prop.state != 'offer_accepted':
                with self.assertRaises(UserError,msg = "Property cant be sold without accepting any offer"):
                    prop.action_sold_btn()
            else:
                prop.action_sold_btn()
                self.assertEqual(prop.state,"sold","Property state should be sold")

    def test_creating_offer_after_sold(self):
        self.properties[1].action_sold_btn()
        with self.assertRaises(UserError,msg="offer cant be created for sold properties"):
            self.env['estate.property.offer'].create([
                {
                    'property_id': self.properties[1].id,
                    'partner_id': self.env.ref('base.res_partner_2').id,
                    'price': 2500000
                }
            ])
