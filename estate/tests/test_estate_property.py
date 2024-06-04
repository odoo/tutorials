from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.estate_property = cls.env['estate.property'].create(
            {
                'name': "property",
                'expected_price': 100,
                'garden_are': 20
            }
        )

    def test_action_sell_without_offer(self):
        with self.assertRaises(UserError):
            self.estate_property.action_sell()

    def test_reset_garden_area_form(self):
        form = Form(self.env['estate.property'])
        form.garden = True
        form.garden_area = 20
        self.assertEqual(form.garden_area, 20)
        form.garden = False
        self.assertEqual(form.garden_area, 0)
