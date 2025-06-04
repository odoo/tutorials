from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tests import tagged


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateOfferTestCase(TransactionCase):

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
                'state': 'new',

            },
            {
                'name': 'Property 2',
                'expected_price': 150000,
                'offer_ids': [
                    (0, 0, {
                        'partner_id': cls.env.ref('base.res_partner_1').id,
                        'price': 120000,
                        'status': 'refused',
                    }),
                    (0, 0, {
                        'partner_id': cls.env.ref('base.res_partner_2').id,
                        'price': 130000,
                    }),
                ],

            },
        ])

    def create_offer_after_sold_property(self):
        """Test that creating an offer on a sold property raises an error."""
        with self.assertRaises(ValidationError):
            self.env['estate.property.offer'].create({
                'property_id': self.properties[0].id,
                'partner_id': self.env.ref('base.res_partner_1').id,
                'price': 110000,
            })

