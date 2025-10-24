from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.cancelled, cls.offer_accepted, cls.sold, cls.new = cls.env['estate.property'].create([
            {'name': 'House1', 'state': 'cancelled', 'living_area': 100},
            {'name': 'House2', 'state': 'offer_accepted', 'living_area': 100, 'garden': True, 'garden_area': 120,
             'garden_orientation': 'north'},
            {'name': 'House3', 'state': 'sold', 'living_area': 150},
            {'name': 'House4', 'state': 'new', 'living_area': 200},
        ])

        cls.env['estate.property.offer'].create(
            [{'price': 100, 'partner_id': cls.env.user.id, 'property_id': cls.offer_accepted.id, 'status': 'accepted'}])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.assertRecordValues(self.offer_accepted, [
            {'name': 'House2', 'total_area': 220},
        ])
        self.offer_accepted.living_area = 20
        self.assertRecordValues(self.offer_accepted, [
            {'name': 'House2', 'total_area': 140},
        ])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.offer_accepted.action_sell()

        self.assertRecordValues(self.offer_accepted, [{'name': 'House2', 'state': 'sold'}])

        with self.assertRaises(UserError):
            self.cancelled.action_sell()

        with self.assertRaises(UserError):
            self.sold.action_sell()

    def test_action_cancel(self):
        """Test that everything behaves like it should when canceling a property."""
        self.offer_accepted.action_cancel()

        self.assertRecordValues(self.offer_accepted, [
            {'name': 'House2', 'state': 'cancelled'},
        ])

        with self.assertRaises(UserError):
            self.sold.action_cancel()

    def test_create_offer_on_sold_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'price': 100,
                'partner_id': self.env.user.id,
                'property_id': self.sold.id,
            }])

    def test_sell_property_without_accepted_offers(self):
        # No offer exists on property
        with self.assertRaises(UserError):
            self.new.action_sell()

        self.env['estate.property.offer'].create([{
            'price': 100,
            'partner_id': self.env.user.id,
            'property_id': self.new.id,
        }])

        # Only pending offer exists on property
        with self.assertRaises(UserError):
            self.new.action_sell()

        self.env['estate.property.offer'].create([{
            'price': 110,
            'partner_id': self.env.user.id,
            'property_id': self.new.id,
            'status': 'accepted'
        }])
        self.new.action_sell()

    def test_reset_garden_area_and_orientation(self):
        self.assertRecordValues(self.offer_accepted,
                                [{'name': 'House2', 'garden': True, 'garden_area': 120, 'garden_orientation': 'north'}])

        with Form(self.offer_accepted) as f1:
            f1.garden = False

        self.assertRecordValues(self.offer_accepted,
                                [{'name': 'House2', 'garden': False, 'garden_area': 0, 'garden_orientation': None}])

        with Form(self.offer_accepted) as f1:
            f1.garden = True

        self.assertRecordValues(self.offer_accepted,
                                [{'name': 'House2', 'garden': True, 'garden_area': 10, 'garden_orientation': 'south'}])
