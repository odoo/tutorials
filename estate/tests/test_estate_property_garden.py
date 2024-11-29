from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install', 'estate_test')
class TestEstatePropertyGarden(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstatePropertyGarden, cls).setUpClass()

    def test_when_garden_toggled_should_reset_orientation_and_area(self):
        wizard = Form(
            self.env['estate.property'].with_context(
                {
                    'name': 'House with garden',
                    'expected_price': 10,
                    'garden': True,
                    'garden_orientation': 'south',
                    'garden_area': 23,
                }
            )
        )

        wizard.garden = False
        self.assertFalse(wizard.garden_orientation)
        self.assertEqual(wizard.garden_area, 0)

        wizard.garden = True
        self.assertEqual(wizard.garden_orientation, 'north')
        self.assertEqual(wizard.garden_area, 10)
