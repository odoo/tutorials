from odoo.tests.common import TransactionCase


class TestEstateProperty(TransactionCase):

    def setUp(self):
        super().setUp()
        self.EstateProperty = self.env['estate.property']
        self.ResUsers = self.env['res.users']

        # Create a test user
        self.test_user = self.ResUsers.create({
            'name': 'Test Salesperson',
            'login': 'test_salesperson',
            'email': 'test_salesperson@example.com',
        })

        # Create another user
        self.other_user = self.ResUsers.create({
            'name': 'Another User',
            'login': 'another_user',
            'email': 'another_user@example.com',
        })

        # Create a property and assign the test user as the salesperson
        self.property = self.EstateProperty.create({
            'name': 'Test Property',
            'description': 'A test property',
            'postcode': '12345',
            'expected_price': 100000,
            'sales_person': self.test_user.id,
        })

    def test_is_current_user_salesperson(self):
        # Log in as the test user
        self.env = self.env(user=self.test_user)

        # Check if the current user is the salesperson
        self.assertEqual(self.property.sales_person, self.env.user, "The current user should be the salesperson")

    def test_is_current_user_not_salesperson(self):
        # Log in as another user
        self.env = self.env(user=self.other_user)

        # Check if the current user is not the salesperson
        self.assertNotEqual(self.property.sales_person, self.env.user, "The current user should not be the salesperson")
