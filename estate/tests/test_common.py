#type:ignore
from odoo.tests.common import TransactionCase
from odoo.tests import tagged


# @tagged('post_install', '-at_install')
class EstateTestCommon(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(EstateTestCommon, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'test Partner'
        })
        cls.property = cls.env['estate.property'].create({
            'name': 'Test Property',
            'status': 'new',
            'expected_price': 100000,
        })
