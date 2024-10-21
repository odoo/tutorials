from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property_new = cls.env['estate.property'].create(
            {
                'name': 'property_new',
                'expected_price': 1000,
                'living_area': 100,
                'state': 'new',
                'garden': True,
                'garden_area': 50,
            },
        )

        cls.property_sold = cls.env['estate.property'].create(
            {
                'name': 'property_sold',
                'expected_price': 2000,
                'living_area': 100,
                'state': 'sold',
            },
        )

        cls.partner_1 = cls.env['res.partner'].create(
            {
                'name': 'partner_1',
            },
        )
