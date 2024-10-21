from odoo.tests import tagged, Form
from .common import EstateTestCase
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class EstateTestCase(EstateTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_total_area_calculation(self):
        """
        Test the total_area field calculation
        """
        self.assertEqual(self.property_new.total_area, self.property_new.living_area + self.property_new.garden_area)
        self.assertEqual(self.property_sold.total_area, self.property_sold.living_area + self.property_sold.garden_area)

    def test_initial_property_state(self):
        with self.assertRaises(UserError):
            self.property_new.action_property_sold()

    def test_make_offers(self):
        self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 850,
            'partner_id': self.partner_1.id,
        })

        self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 1100,
            'partner_id': self.partner_1.id,
        })

        offer_high = self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 1650,
            'partner_id': self.partner_1.id,
        })

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property_new.id,
                'price': 1150,
                'partner_id': self.partner_1.id,
            })

        self.assertEqual(self.property_new.state, 'offer_received')
        self.assertEqual(self.property_new.best_price, offer_high.price)

        with self.assertRaises(UserError):
            self.property_new.action_property_sold()

    def test_accept_offer(self):
        offer_low = self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 850,
            'partner_id': self.partner_1.id,
        })
        offer_normal = self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 1100,
            'partner_id': self.partner_1.id,
        })
        offer_high = self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 1650,
            'partner_id': self.partner_1.id,
        })
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property_new.id,
                'price': 1500,
                'partner_id': self.partner_1.id,
            })

        offer_normal.action_accept_offer()

        self.assertEqual(self.property_new.state, 'offer_accepted')
        self.assertEqual(offer_normal.status, 'accepted')
        self.assertEqual(offer_low.status, 'refused')
        self.assertEqual(offer_high.status, 'refused')
        self.assertEqual(self.property_new.selling_price, offer_normal.price)

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property_new.id,
                'price': 1500,
                'partner_id': self.partner_1.id,
            })

        with self.assertRaises(UserError):
            offer_high.action_accept_offer()

    def test_sell_property(self):
        offer_normal = self.env['estate.property.offer'].create({
            'property_id': self.property_new.id,
            'price': 1100,
            'partner_id': self.partner_1.id,
        })

        offer_normal.action_accept_offer()
        self.property_new.action_property_sold()
        self.assertEqual(self.property_new.state, 'sold')

        with self.assertRaises(UserError):
            self.property_new.action_property_sold()

    def test_onChange_garden(self):
        property_form = Form(self.env['estate.property'])
        self.assertEqual(property_form.garden_area, 0)
        self.assertEqual(property_form.garden_orientation, False)

        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, 'north')
        self.assertEqual(property_form.total_area, property_form.living_area + property_form.garden_area)

        property_form.garden = False
        self.assertEqual(property_form.garden_area, 0)
        self.assertEqual(property_form.garden_orientation, False)
        self.assertEqual(property_form.total_area, property_form.living_area)
