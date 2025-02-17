from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env["estate.property"].create([
            {
                'name': 'Villa on the beach',
                'expected_price': 1000000,
                'living_area': 100,
            },
            {
                'name': 'Apartment in the city',
                'expected_price': 500000,
                'living_area': 50,
            }
        ])

        # cls.offers = cls.env["estate.property.offer"].create({
        #     'partner_id': cls.env.ref('base.res_partner_12').id,
        #     'property_id': cls.properties[0].id,
        #     'price': 1000000,
        # })

        # cls.properties[0].property_ids = cls.offers.id


    def test_creation_area(self):
        """"Test that the total_area is computed like it should."""

        self.assertRecordValues(self.properties, [
            {'name': 'Villa on the beach', 'expected_price': 1000000,
             'total_area': 100},
            {'name': 'Apartment in the city',
                'expected_price': 500000, 'total_area': 50},
        ])

    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties[0].action_sold_property()
        self.assertEqual(self.properties[0].state, 'sold')

        # with self.assertRaises(UserError):
        #     self.properties.forbidden_action_on_sold_property()

    def test_create_offer_for_sold_property(self):
        """Test that we cannot create an offer for a sold property."""
        self.properties[0].action_sold_property()
        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create({
                'partner_id': self.env.ref('base.res_partner_12').id,
                'property_id': self.properties[0].id,
                'price': 1000000,
            })
    
    # def test_sold_property_without_offer(self):
    #     """Test that we cannot sell a property without an accepted offer."""
    #     with self.assertRaises(UserError):
    #         self.properties[1].action_sold_property()
