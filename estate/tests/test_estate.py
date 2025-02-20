from odoo import Command
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged, Form


@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()
        cls.partners = cls.env['res.partner'].create([{
           'name': 'Dumb Person',
        }])
        cls.properties = cls.env['estate.property'].create([
            {
                'name': 'Small Villa',
                'offer_ids': [
                    Command.create({
                        'partner_id': cls.partners[0].id,
                        'price': 9999.0
                    }),
                ],
            }
        ])

    def test_creation_offer(self):
        self.properties[0].state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'partner_id': self.partners[0].id,
                'price': 999999.0,
                'property_id': self.properties[0].id
            })

    def test_sell_property(self):
        self.properties.state = 'received'
        with self.assertRaises(UserError):
            self.properties.action_sold()
        self.properties.state = 'accepted'
        self.properties.action_sold()
        self.assertRecordValues(self.properties, [
            {'state': 'sold'}
        ])

    def test_reset_garden(self):
        form = Form(self.env['estate.property'])
        form.name = 'Test Property'
        form.garden = True
        property = form.save()
        self.assertRecordValues(property, [
            {'garden': True, 'garden_area': 10, 'garden_orientation': 'north'}
        ])
        form.garden = False
        property = form.save()
        self.assertRecordValues(property, [
            {'garden': False, 'garden_area': 0, 'garden_orientation': False}
        ])
