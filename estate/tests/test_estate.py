from odoo.exceptions import UserError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.property = cls.env['estate.property'].create({
            'name': 'property',
            'state': 'new',
            'expected_price': 100000,
        })

    def test_prevent_offer_creation_on_property(self):
        self.property.state = 'sold'
        self.assertEqual(self.property.state, 'sold')

        with self.assertRaises(UserError):
            self.property.offer_ids.create([{
                'partner_id': self.env.uid,
                'property_id': self.property.id,
                'price': 100000,
            }])

    def test_prevent_sale_without_offer(self):
        self.assertEqual(len(self.property.offer_ids), 0, 'Property should not have any offers')
        with self.assertRaises(UserError):
            self.property.action_mark_as_sold()

    def test_mark_property_as_sold(self):
        self.property.offer_ids.create([{
            'partner_id': self.env.uid,
            'property_id': self.property.id,
            'price': 100000,
        }])
        self.property.action_mark_as_sold()
        self.assertEqual(self.property.state, 'sold', 'Property should have been updated to sold state')

    def test_property_form_garden_reset(self):
        form = Form(self.env['estate.property'])
        form.name = 'Garden Test Property'
        form.expected_price = 10000

        form.garden = True
        property_with_garden = form.save()
        self.assertEqual(property_with_garden.garden, True)
        self.assertEqual(property_with_garden.garden_area, 10)
        self.assertEqual(property_with_garden.garden_orientation, 'north')

        form.garden = False
        property_without_garden = form.save()
        self.assertEqual(property_without_garden.garden, False)
        self.assertEqual(property_without_garden.garden_area, 0)
        self.assertEqual(property_without_garden.garden_orientation, False)
