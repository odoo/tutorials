from odoo.addons.estate.tests.common import EstateTestCommon
from odoo.tests.common import Form
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestCheckGarden(EstateTestCommon):

    def test_check_garden(self):
        property_form = Form(self.env['estate.property'])

        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, "north")

        property_form.garden = False
        self.assertEqual(property_form.garden_area, 0)
        self.assertEqual(property_form.garden_orientation, False)
