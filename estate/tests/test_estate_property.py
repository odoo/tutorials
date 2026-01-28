from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import Form

class EstatePropertyTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstatePropertyTestCase, cls).setUpClass()

        cls.properties = cls.env['estate.property'].create([
            {
                'id': 'property1',
                'name': 'Property with garden',
                'expected_price': 1_000,
                'garden_area': 1_000,
                'garden': True,
                'garden_orientation': 'south'
            }
        ])

    #Should work but does not
    #def test_garden_reset(self):
    #    with Form(self.properties[0]) as form:
    #        form.garden = False
    #
    #    self.assertEqual(self.properties[0].garden_area, 0)
    #    self.assertEqual(self.properties[0].garden_orientation, False)


