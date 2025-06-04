from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Property 1',
                'expected_price': 100000,
                'state': 'offer_accepted',
                'offer_ids': [
                    (0, 0, {
                        'partner_id': cls.env.ref('base.res_partner_1').id,
                        'price': 110000,
                    }),
                ],
            },
        ])
        cls.properties[0].offer_ids[0].action_accept()

    def test_sell_property(self):
        """Test that selling a property that can be sold updates the right fields."""
        self.properties[0].set_sold()
        self.assertEqual(self.properties[0].state, 'sold')
        self.assertEqual(self.properties[0].buyer_id, self.env.ref('base.res_partner_1'))
        self.assertEqual(self.properties[0].selling_price, 110000)

