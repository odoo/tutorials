from odoo.tests.common import TransactionCase


class TestEstatePropertyCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestEstatePropertyCommon, cls).setUpClass()
        cls.contact_company_1 = cls.env['res.partner'].create(
            {
                'name': 'Planet Express',
                'email': 'planetexpress@example.com',
                'is_company': True,
                'street': '57th Street',
                'city': 'New New York',
                'country_id': cls.env.ref('base.us').id,
                'zip': '12345',
            }
        )

        cls.contact_1 = cls.env['res.partner'].create(
            {
                'name': 'Philip J Fry',
                'email': 'philip.j.fry@test.example.com',
                'mobile': '+1 202 555 0122',
                'title': cls.env.ref('base.res_partner_title_mister').id,
                'function': 'Delivery Boy',
                'phone': False,
                'parent_id': cls.contact_company_1.id,
                'is_company': False,
                'street': 'Actually the sewers',
                'city': 'New York',
                'country_id': cls.env.ref('base.us').id,
                'zip': '54321',
            }
        )

        cls.property_1 = cls.env['estate.property'].create(
            {
                'name': 'Property Without Offers',
                'expected_price': 10,
                'state': 'new',
            }
        )

        cls.property_2 = cls.env['estate.property'].create(
            {
                'name': 'Property With Sold Status',
                'state': 'sold',
                'expected_price': 10,
            }
        )

        cls.property_3 = cls.env['estate.property'].create(
            {
                'name': 'Property That Can Be Sold',
                'expected_price': 10,
                'state': 'received',
            }
        )

        cls.property_4 = cls.env['estate.property'].create(
            {
                'name': 'Cancelled Property',
                'state': 'cancelled',
                'expected_price': 10,
            }
        )

        cls.offers = cls.env['estate.property.offer'].create(
            [
                {
                    'property_id': cls.property_3.id,
                    'price': 9,
                    'partner_id': cls.contact_1.id,
                }
            ]
        )
