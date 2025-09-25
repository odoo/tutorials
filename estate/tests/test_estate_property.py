from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.tests import Form


class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_model = cls.env['estate.property']
        cls.offer_model = cls.env['estate.property.offer']
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Buyer',
            'email': 'buyer@example.com',
        })

    def _create_property(self, **extra_vals):
        vals = {
            'name': 'Test Property',
            'expected_price': 200000,
        }
        vals.update(extra_vals)
        return self.property_model.create(vals)

    def test_offer_not_allowed_on_sold_property(self):
        property_record = self._create_property(state='sold')

        with self.assertRaises(UserError):
            self.offer_model.create({
                'price': 210000,
                'property_id': property_record.id,
                'partner_id': self.partner.id,
            })

    def test_cannot_sell_property_without_accepted_offer(self):
        property_record = self._create_property()

        with self.assertRaises(UserError):
            property_record.action_set_sold()

    def test_property_marked_sold_when_allowed(self):
        property_record = self._create_property()
        offer = self.offer_model.create({
            'price': 210000,
            'property_id': property_record.id,
            'partner_id': self.partner.id,
        })
        offer.action_accept_offer()

        property_record.action_set_sold()
        self.assertEqual(property_record.state, 'sold')

    def test_garden_reset_on_form_toggle(self):
        with Form(self.env["estate.property"]) as property_form:
            property_form.name = 'Garden Property'
            property_form.expected_price = 250000
            property_form.garden = True
            self.assertEqual(property_form.garden_area, 10)
            self.assertEqual(property_form.garden_orientation, 'north')
            property_form.garden = False
            self.assertEqual(property_form.garden_area, 0)
            self.assertFalse(property_form.garden_orientation)
            property_record = property_form.save()

        self.assertFalse(property_record.garden)
        self.assertEqual(property_record.garden_area, 0)
        self.assertFalse(property_record.garden_orientation)
