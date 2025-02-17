from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form

@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env['estate.property'].create({
            'name': 'Test Property',
            'description': 'Test Property Description',
            'expected_price': 100000,
            'state': 'new',
            'garden': True,
            'garden_area': 50.0,
            'garden_orientation': 'north',
        })

    # def test_create_property(self):
    #     self.properties.living_area = 20
    #     self.assertRecordValues(self.properties, [
    #         {'name': 'Test Property', 'total_area': 70},
    #     ])

    def test_action_sell(self):

        offer = self.env['estate.property.offer'].create({
            'property_id': self.properties.id,
            'price': 100052,
            'partner_id': self.env.ref('base.res_partner_1').id,
        })

        self.assertRecordValues(self.properties, [
            {'name': 'Test Property', 'state': 'offer_received'},
        ])

        with self.assertRaises(UserError, msg="Selling without an offer should raise a UserError"):
            self.properties.action_sold()
            print("After First Sold")


        offer.action_accept_offer()
        self.assertRecordValues(self.properties, [
            {'name': 'Test Property', 'state': 'offer_accepted'},
        ])

        self.properties.action_sold()
        self.assertRecordValues(self.properties, [
            {'name': 'Test Property', 'state': 'sold'},
        ])

    def test_garden_checkbox_behavior(self):

        form = Form(self.properties)

        initial_garden_area = form.garden_area
        initial_orientation = form.garden_orientation

        form.garden = False

        self.assertEqual(form.garden_area, initial_garden_area, "Garden Area should not be reset.")
        self.assertEqual(form.garden_orientation, initial_orientation, "Orientation should not be reset.")

        self.assertFalse(form.garden, "Garden checkbox should be unchecked.")
