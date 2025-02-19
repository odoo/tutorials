from odoo.tests.common import TransactionCase
from odoo.tests import Form
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.fields import Command

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.property = cls.env['estate.property'].create({
            'name': 'Luxury Villa',
            'state': 'new',
        })

        cls.property1 = cls.env['estate.property'].create({
            'name': 'No offer Villa',
            'state': 'new',
        })

        cls.partner = cls.env.ref('base.res_partner_12') 
        cls.offer = cls.env['estate.property.offer'].create({
            'property_id': cls.property.id,
            'price': 450000,
            'status': 'accepted',
            'partner_id': cls.partner.id
        })

    def test_create_offer_for_sold_property(self):
        self.property.state = 'sold'

        with self.assertRaises(UserError,msg="Create offer for sold property"):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'price': 400000,
                'partner @classmethod_id': self.partner.id
            })

    def test_sell_property_without_accepted_offer(self):
        with self.assertRaises(UserError, msg="Sell property without accepted offer"):
            self.property1.action_set_sold()

    def test_sell_property_with_accepted_offer(self):
        self.property.state = 'offer_accepted'
        self.property.action_set_sold()
        self.assertEqual(self.property.state, 'invoiced', "The property should be marked as Invoiced.")

class GardenCheck(Form):
    @classmethod
    def setUpClass(cls):
        super(GardenCheck, cls).setUpClass()

    def test_garden_checkbox_reset(self):
        if(self.garden == False):
            self.assertEqual(self.property.garden_area, 0 , "Garden Area should be reset to False")
            self.assertEqual(self.property.orientation, False, "Orientation should be reset to False")
