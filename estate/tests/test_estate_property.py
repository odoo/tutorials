from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests import Form
from odoo.tests.common import users
from odoo.tests.common import new_test_user

@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstatePropertyTestCase, cls).setUpClass()
        cls.test_user = new_test_user(cls.env, login='estate_test_user', groups='estate.estate_group_manager')
        cls.property = cls.env['estate.property'].create({
                                                            'name': 'Test',
                                                            'expected_price': '1',
                                                            })

    def test_sell_no_offers(self):
        """Test that a property cannot be sold when there are no accepted offers: no offers at all."""
        self.property.offer_ids = []
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_sell_no_accepted_offers(self):
        """Test that a property cannot be sold when there are no accepted offers: some unaccepted offers are present."""
        offers = [
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': 1,  # Trying to avoid having to create a new (irrelevant) res.partner record, appears to work
                'price': 1,
            }),
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': 1,
                'price': 1,
                'state': 'refused'
            }),
        ]
        self.property.offer_ids = [offer.id for offer in offers]
        with self.assertRaises(UserError):
            self.property.action_set_sold()

    def test_sell_sets_sold(self):
        """Test that selling a property sets it to 'Sold'."""
        offers = [
            self.env['estate.property.offer'].create({
                'property_id': self.property.id,
                'partner_id': 1,
                'price': 1,
            }),
        ]
        self.property.offer_ids = [offer.id for offer in offers]
        offers[0].action_accept()
        self.property.action_set_sold()
        self.assertEqual(self.property.state, 'sold')

    @users('estate_test_user')
    def test_garden_set_to_true(self):
        """Test that checking the 'Garden' field on the form updates garden-related values."""
        with Form(self.property) as property_form:
            property_form.garden = True
        self.assertRecordValues(self.property, [
            {'garden_area': 10, 'garden_orientation': 'north'}
        ])

    @users('estate_test_user')
    def test_garden_set_to_false(self):
        """Test that unchecking the 'Garden' field on the form resets garden-related values."""
        self.property.garden = True
        self.property.garden_area = 1
        self.property.garden_orientation = 'south'
        with Form(self.property) as property_form:
            property_form.garden = False
        self.assertRecordValues(self.property, [
            {'garden_area': 0, 'garden_orientation': None}
        ])
