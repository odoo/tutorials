from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):

        super(EstateTestCase, cls).setUpClass()
        cls.properties = cls.env['estate.property'].create([...])
