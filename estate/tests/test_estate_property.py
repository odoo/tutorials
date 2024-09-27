from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests.common import tagged, Form


@tagged('post_install', '-at_install')
class TestEstateProperty(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env['estate.property'].create({
            'name': 'test property',
            'expected_price': 500000,
            'state': 'new',
        })
        cls.res_partner = cls.env['res.partner'].create({
            'name': 'test partner',
        })

    def test_compute_total_area(self):
        """Test that the total_area is correctly computed"""
        self.properties.living_area = 20
        self.properties.garden = True
        self.properties.garden_area = 20
        self.assertRecordValues(self.properties, [
            {
                'name': 'test property',
                'total_area': 40,
            },
        ])

    def test_create_offer_on_sold(self):
        """Creating an offer on a sold property should not be possible."""
        self.properties.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 450000,
                'property_id': self.properties.id,
                'partner_id': self.res_partner.id,
            })
        self.properties.state = 'new'

    def test_sell_without_accepted_offer(self):
        """Selling a property without an accepted offer should not be possible."""
        with self.assertRaises(UserError):
            self.properties.action_set_sold()

    def test_garden_checkbox_unchecked(self):
        """Test that the garden orientation and area are not reset after unchecking the garden checkbox"""

        with Form(self.properties) as property_form:
            property_form.garden = True
            property_form.garden_area = 100
            property_form.garden_orientation = "north"

            property_form.garden = False

        self.assertEqual(self.properties.garden_area, 100)
        self.assertEqual(self.properties.garden_orientation, "north")
