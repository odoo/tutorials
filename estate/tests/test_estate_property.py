# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import Form, TransactionCase


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create(
            [
                {'name': 'Property 1', 'expected_price': 100000, 'garden_area': 0},
                {'name': 'Property 2', 'expected_price': 100000, 'garden_area': 50},
            ]
        )
        cls.canceled_property = cls.env['estate.property'].create(
            {'name': 'Canceled Property', 'expected_price': 100000}
        )
        cls.property_without_offer = cls.env['estate.property'].create(
            {'name': 'Property without offer', 'expected_price': 100000}
        )

        # Populate properties with offers
        cls.partner = cls.env['res.partner'].create({'type': 'contact', 'name': 'Partner 1'})
        for property_model in [*cls.properties, cls.canceled_property]:
            cls.env['estate.property.offer'].create(
                {
                    'property_id': property_model.id,
                    'price': property_model.expected_price,
                    'partner_id': cls.partner.id,
                }
            )

        cls.canceled_property.state = 'canceled'

    def test_total_area(self):
        """
        total area is computed as the sum of garden_area + living_area
        """
        self.properties.living_area = 50
        self.assertRecordValues(
            self.properties,
            [
                {'total_area': 50},
                {'total_area': 100},
            ],
        )

    def test_action_sell(self):
        self.properties.action_sell()
        self.assertRecordValues(
            self.properties,
            [
                {'state': 'sold'},
                {'state': 'sold'},
            ],
        )

        with self.assertRaises(UserError):
            self.canceled_property.action_sell()

        with self.assertRaises(UserError):
            self.property_without_offer.action_sell()

    def test_form_garden_area_reset(self):
        form = Form(self.properties[1])
        self.assertEqual(form.garden_area, 50)
        form.garden = False
        self.assertEqual(form.garden_area, 0)
        form.garden = True
        self.assertEqual(form.garden_area, 10)
