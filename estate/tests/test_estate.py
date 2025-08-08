from odoo import Command

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests import Form

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.properties = cls.env["estate.property"].create(
            {
                'name': 'Property 1',
                'expected_price': 100000,
            },
        )

        cls.properties[0].offer_ids = [Command.create(
                {
                    'partner_id': cls.env.ref(xml_id="base.res_partner_12").id,
                    'price': 120000,
                },
            )]

    def test_accept_offer(self):
        with self.assertRaises(UserError):
            self.properties[0].action_set_sold()

        self.properties[0].offer_ids.action_set_accepted()

        self.properties[0].action_set_sold()

        self.assertRecordValues(self.properties, [
            {'state': 'sold'},
        ])

        with self.assertRaises(UserError):
            self.properties[0].offer_ids = [Command.create(
                {
                    'partner_id': self.env.ref(xml_id="base.res_partner_12").id,
                    'price': 140000,
                },
            )]

    def test_property_form(self):
        with Form(self.properties[0]) as prop:
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)

            prop.garden = True
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "north")

            prop.garden = False
            self.assertEqual(prop.garden_area, 0)
            self.assertFalse(prop.garden_orientation)
