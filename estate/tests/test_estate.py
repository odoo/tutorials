from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged


@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner1 = cls.env['res.partner'].create({
            'name': 'Customer1',
        })

        cls.partner2 = cls.env['res.partner'].create({
            'name': 'Customer2',
        })

        cls.property_a = cls.env['estate.property'].create({
            'name': 'Apartment1',
            'expected_price': 1000,
            'garden': True,
        })

        cls.offer_a_1 = cls.env['estate.property.offer'].create({
            'price': 920,
            'property_id': cls.property_a.id,
            'partner_id': cls.partner1.id,
        })

        cls.offer_a_2 = cls.env['estate.property.offer'].create({
            'price': 950,
            'property_id': cls.property_a.id,
            'partner_id': cls.partner2.id,
        })

    def test_create_offer_for_sold_property(self):
        """Test that one cannot create an offer for a sold property"""
        self.property_a.state = 'sold'

        with self.assertRaises(UserError):
            self.offer_a_1.action_accept()

    def test_action_sold(self):
        """Test that everything behaves like it should when selling a property."""
        with self.assertRaises(UserError):
            self.property_a.action_set_sold()

        self.offer_a_1.action_accept()

        self.property_a.action_set_sold()

        self.assertRecordValues(self.property_a, [
            {'state': 'sold'},
        ])

    def test_garden_checkbox_uncheck(self):
        """Test resetting of garden properties when checkbox is unchecked"""
        self.property_a.garden_area = 100
        self.property_a.garden_orientation = 'north'

        # with Form(self.env['estate.property']) as form:
        #     form.garden = False

        estate_form = Form(self.property_a)
        estate_form.garden = False
        estate_form.save()

        self.assertRecordValues(self.property_a, [
            {'garden': False, 'garden_area': False, 'garden_orientation': False},
        ])
