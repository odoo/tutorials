from odoo.tests import Form, TransactionCase, tagged


@tagged('post_install', '-at_install')
class EstateGardenTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100000,
        })

    def test_garden_onchange(self):
        """Unchecking the garden resets its area and orientation."""
        with Form(self.property) as form:
            form.garden = True
            self.assertEqual(form.garden_area, 10)
            self.assertEqual(form.garden_orientation, 'north')
            form.garden = False
            self.assertEqual(form.garden_area, 0)
            self.assertFalse(form.garden_orientation)
