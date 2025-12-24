from odoo.exceptions import UserError
from odoo.tests import tagged, Form
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create(
            {
                'name': "Test property 1",
                'expected_price': 100000,
            },
        )
        cls.property.offer_ids.create({
            'property_id': cls.property.id,
            'partner_id': cls.env['res.partner'].create({'name': "Test partner"}).id,
            'price': 100000,
        })

    def test_cannot_create_offer_for_sold_property(self):
        self.property.offer_ids.action_confirm()
        self.property.action_set_sold()
        with self.assertRaises(UserError):
            self.property.offer_ids.create({
                'property_id': self.property.id,
                'partner_id': self.env['res.partner'].create({'name': "Test partner 2"}).id,
                'price': 100000,
            })

    def test_cannot_sell_property_with_no_accepted_offers_on_it(self):
        self.property.offer_ids.action_refuse()
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_sold_property_has_sold_status(self):
        self.property.offer_ids.action_confirm()
        self.property.action_set_sold()
        self.assertEqual(self.property.state, 'sold')

    def test_unchecking_garden_checkbox_does_not_break(self):
        with Form(self.property) as property_form:
            # Uncheck and check box again
            property_form.garden = False
            property_form.garden = True

            self.assertEqual(property_form.garden_area, 10)
            self.assertEqual(property_form.garden_orientation, 'north')
