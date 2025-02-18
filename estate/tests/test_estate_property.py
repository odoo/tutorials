from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        
        cls.property = cls.env['estate.property'].create(
            {
                'name': 'Test Property',
                'description': 'A beautiful test property for unit tests.',
                'living_area': 150,
                'garden': True,
                'garden_area': 50,
                'garden_orientation': 'east',
                'status': 'offer_accepted',
                'expected_price': 100000,
            }
        )
        cls.property_1 = cls.env['estate.property'].create(
            {
                'name': 'Test Property 2',
                'description': 'A beautiful test property for unit tests.',
                'living_area': 150,
                'garden': True,
                'garden_area': 50,
                'garden_orientation': 'east',
                'status': 'offer_accepted',
                'expected_price': 100000,
            }
        )
        cls.property_2 = cls.env['estate.property'].create(
            {
                'name': 'Test Property 3',
                'description': 'A beautiful test property for unit tests.',
                'living_area': 150,
                'status': 'new',
                'expected_price': 100000,
            }
        )
        cls.accepted_offer = cls.env['estate.property.offer'].create(
            {
                'property_id': cls.property.id,
                'partner_id': cls.env.ref('base.partner_demo').id,
                'price': 100000,
                'status': 'accepted',
            }
        )

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.property.living_area = 150
        self.assertRecordValues(
            self.property,
            [{'name': 'Test Property', 'total_area': 200}]
        )

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.property.action_mark_as_sold()
        self.assertRecordValues(self.property, [
            {'name': 'Test Property 2', 'status': 'sold'},
        ])

    def test_action_sell_no_offer(self):
        """Test that a property cannot be sold if no accepted offers are present."""
        with self.assertRaises(UserError):
            self.property_1.action_mark_as_sold()

    def test_create_offer_for_sold_property(self):
        """Test that no offer can be created for a sold property."""
        self.property_1.action_mark_as_sold()
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.property_1.id,
                'partner_id': self.env.ref('base.partner_demo').id,
                'price': 150000,
            })

    def test_sell_property_correctly_marked_sold(self):
        """Test that selling a property with an accepted offer correctly marks it as sold."""
        self.property.action_mark_as_sold()
        self.assertRecordValues(self.property, [
            {'name': 'Test Property', 'status': 'sold'},
        ])

    def test_garden_area_reset_on_uncheck(self):
        """Ensure Garden Area and Orientation reset when the Garden checkbox is unchecked."""
        self.property_2.garden = True
        self.property_2.garden_area = 100
        self.property_2.garden_orientation = 'north'
        
        self.property_2.garden = False
        self.property_2._onchange_garden()

        self.assertEqual(self.property_2.garden_area,0)
        self.assertEqual(self.property_2.garden_orientation, False)
