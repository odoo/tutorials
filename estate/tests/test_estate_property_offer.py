from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import Form


@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstatePropertyOfferTestCase, cls).setUpClass()

        cls.property = cls.env['estate.property'].create({
            'name': 'Test property',
            'expected_price': 100000,
        })

        cls.offer = {
            'price': 110000,
            'property_id': cls.property.id,
            'partner_id': cls.env.uid
        }

    
    def test_creation_data(self):
        self.assertEqual(self.property.name, 'Test property')
        self.assertEqual(self.property.expected_price, 100000.0)

    def test_no_sale_if_property_has_no_offers(self):
        self.assertEqual(len(self.property.offer_ids), 0)
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_deny_offer_creation_on_sold_property(self):
        self.property.state = 'sold'
        self.assertEqual(self.property.state, 'sold')

        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create(self.offer)

    def test_mark_property_as_sold_on_valid_sale(self):
        self.property.state = 'offer_accepted'
        self.assertEqual(self.property.state, 'offer_accepted')

        self.env['estate.property.offer'].create(self.offer)
        self.property.action_sold()

        self.assertEqual(self.property.state, 'sold')

    def test_garden_checkbox_reset(self):
        form = Form(self.env['estate.property'])
        form.garden = True
        form.garden_area = 20
        form.garden_orientation = 'N'

        property_with_garden = form.save()

        self.assertEqual(property_with_garden.garden, True)
        self.assertEqual(property_with_garden.garden_area, 20)
        self.assertEqual(property_with_garden.garden_orientation, 'N')

        form.garden = False
        property_without_garden = form.save()
        
        self.assertEqual(property_without_garden.garden, False)
        self.assertEqual(property_without_garden.garden_area, 0)
        self.assertEqual(property_without_garden.garden_orientation, False)
