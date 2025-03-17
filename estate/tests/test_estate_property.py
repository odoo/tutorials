from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env['estate.property'].create(
            {
                'name': 'Test Property',
                'expected_price': 100000.0,
                'postcode': '12345',
                'bedrooms': 3,
                'living_area': 100,
                'facades': 2,
                'garage': True,
                'garden': True,
                'garden_area': 20,
            }
        )

        cls.test_partner = cls.env['res.partner'].create(
            {
                'name': 'Test Partner'
            }
        )

    def test_create_offer_for_sold_property(self):

        self.property.write({'state': 'sold'})
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create(
                {
                    'price': 123456,
                    'partner_id': self.test_partner.id,
                    'property_id': self.property.id
                }
            )

    def test_sell_property_with_no_buyer(self):

        self.property.write({'state': 'new'})
        with self.assertRaises(UserError):
            self.property.action_sold()

        self.offer = self.env['estate.property.offer'].create(
            {
                    'price': 123456,
                    'partner_id': self.test_partner.id,
                    'property_id': self.property.id
            }
        )[0]

        self.offer.action_accept()
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold', "Property should be in offer accepted state")


    def test_check_garden_property(self):

        form = Form(self.property)

        self.assertTrue(form.garden)
        self.assertEqual(form.garden_area, 20)
        self.assertEqual(form.garden_orientation, 'north')

        form.garden = False
        form.save()

        self.assertEqual(form.garden, False)
        self.assertEqual(form.garden_area, 0)
        self.assertEqual(form.garden_orientation, False)

        form.garden = True
        form.save()

        self.assertEqual(form.garden, True)
        self.assertEqual(form.garden_area, 10)
        self.assertEqual(form.garden_orientation, 'north')
