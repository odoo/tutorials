from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestPricelistBase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        TestUsersEnv = cls.env['res.users'].with_context({'no_reset_password': True})
        cls.country_belgium = cls.env.ref('base.be')
        group_portal_id = cls.env.ref('base.group_portal').id
        cls.user_portal = TestUsersEnv.create({
            'name': 'Beatrice Portal',
            'login': 'Beatrice',
            'country_id': cls.country_belgium.id,
            'email': 'beatrice.employee@example.com',
            'groups_id': [(6, 0, [group_portal_id])],
        })

        cls.pricelist = cls.env['product.pricelist'].create({'name': 'Base Test Pricelist'})
