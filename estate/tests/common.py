from odoo.tests.common import TransactionCase


class EstateTestCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner_1 = cls.env['res.partner'].create({
            'name': 'partner_1',
            'email': 'partner_1',
            'company_id': False
        })

        cls.property_1 = cls.env['estate.property'].create({
            'name': 'Test Property',
            'expected_price': 100,
            'garden_orientation': 'north',
            'state': 'new',
            'best_price': 0
        })

        cls.property_2 = cls.env['estate.property'].create({
            'name': 'Test Property 2',
            'expected_price': 200,
            'garden_orientation': 'north',
            'state': 'sold',
            'best_price': 0
        })
