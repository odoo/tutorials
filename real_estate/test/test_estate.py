from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create({
            'state': 'new',
            'has_garden': True,
            'garden_area': 50,
            'garden_orientation': 'south',
        })
        cls.offer = cls.env['estate.property.offer'].create({
            'price': 800000,
            'property_id': cls.property.id,
            'validity': 15,
            'partner_id': cls.partner.id
        })

    def test_prevent_offer_on_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'state': 'new',
            })

    def test_prevent_selling_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_selling_property_marks_as_sold(self):
        self.offer.state = 'accepted'
        self.property.action_sold()
        self.assertEqual(self.property.state, 'sold', "The property should be marked as sold.")

    def test_reset_garden_fields(self):
        self.property.garden = False
        self.assertEqual(self.property.garden_area, 0, "Garden area should be reset to 0.")
        self.assertFalse(self.property.garden_orientation, "Garden orientation should be reset to False.")
