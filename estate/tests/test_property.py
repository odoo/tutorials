from odoo.tests import TransactionCase, Form
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
            'garden': True,
            'garden_area': 50,
            'orientation': 'north',
        })

        cls.buyer = cls.env['res.partner'].create({'name': 'Test Buyer'})

        cls.offer = cls.env['estate.property.offer'].create({
            'property_id': cls.property.id,
            'partner_id': cls.buyer.id,
            'price': 95000,
        })

    def test_offer_on_sold_property(self):
        self.property.state = 'sold'
        self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.buyer.id,
            'price': 110000,
        })

        with self.assertRaises(UserError):
            self.offer.action_accept()

    def test_successful_property_sale(self):
        offer = self.env['estate.property.offer'].create({
            'property_id': self.property.id,
            'partner_id': self.buyer.id,
            'price': 110000,
        })
        offer.action_accept()
        self.property.action_sold()

        self.assertEqual(self.property.state, 'sold')
        self.assertEqual(self.property.buyer_id, self.buyer)
        self.assertEqual(self.property.selling_price, offer.price)

    def test_garden_uncheck_reset(self):
        with Form(self.property) as form:
            self.assertTrue(form.garden)
            self.assertEqual(form.garden_area, 50)
            self.assertEqual(form.orientation, 'north')

            form.garden = False
            form.save()

        self.property.invalidate_recordset()
        self.assertFalse(self.property.garden, "Garden should be unchecked.")
        self.assertEqual(self.property.garden_area, 0, "Garden area should reset to 0.")
        self.assertFalse(self.property.orientation, "Orientation should reset to False or empty.")
