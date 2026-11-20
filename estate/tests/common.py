from odoo.tests import TransactionCase
from odoo.tests import tagged, TransactionCase


@tagged('post_install', '-at_install')
class EstatePropertyTestCommon(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(EstatePropertyTestCommon, cls).setUpClass()

        cls.base_property = cls.env['estate.property'].create({
            'name': 'BaseProperty',
            'expected_price': 100_000,
        })
