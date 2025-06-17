from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo import Command


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        cls.property = cls.env['estate.property'].create([{'name': 'test_house'}])
        cls.partner = cls.env['res.partner'].create([{
            'name': 'test_person',
        }])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.property.living_area = 20
        self.property.garden = True
        self.property.garden_area = 15

        self.assertEqual(self.property.total_area, 35)

    def test_action_sell_without_accepted_offer(self):
        """Test that everything behaves like it should when selling an invalid property."""

        self.assertEqual(self.property.state, 'new')

        with self.assertRaises(UserError):
            self.property.action_property_sold()

    def test_action_sell_with_accepted_offer(self):
        """Test that everything behaves like it should when selling a valid property."""

        self.property.offer_ids.create({
            'property_id': self.property.id,
            'partner_id': self.partner.id,
            'price': 124,
            'validity': 14,
        })
        self.property.offer_ids.action_offer_accept()
        self.property.action_property_sold()

        self.assertRecordValues(self.property, [
           {'state': 'sold'},
        ])

    def test_creation_offer_for_sold_property(self):
        """Test that everything behaves like it should when property is sold."""

        self.property.write({'offer_ids': [Command.create({
            'partner_id': self.partner.id,
            'price': 124,
            'validity': 14,
        })]})
        self.property.offer_ids.action_offer_accept()
        self.property.action_property_sold()

        with self.assertRaises(UserError):
            self.property.offer_ids.create({
                'property_id': self.property.id,
                'partner_id': self.partner.id,
                'price': 130,
                'validity': 14,
            })

    def test_enable_garden(self):
        """Test that default values are assigned to garden area and orientation when garden is enabled"""

        form = Form(self.env['estate.property'])
        form.garden = True

        self.assertEqual(form.garden_area, 10)
        self.assertEqual(form.garden_orientation, 'north')

    def test_disable_garden(self):
        """Test that values are removed from garden area and orientation when garden is disabled"""

        form = Form(self.env['estate.property'])
        form.garden = True
        form.garden_area = 15
        form.garden_orientation = 'south'
        form.garden = False

        self.assertEqual(form.garden_area, 0)
        self.assertEqual(form.garden_orientation, False)
