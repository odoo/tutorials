from odoo.fields import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestOneTimeSaleCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Set up common test data."""
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Pricelist',
        })
        cls.plan_monthly = cls.env['sale.subscription.plan'].create({
            'name': 'Monthly Plan',
            'billing_period_unit': 'week'
        })
        cls.plan_yearly = cls.env['sale.subscription.plan'].create({
            'name': 'Yearly Plan',
            'billing_period_unit': 'year'
        })

        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.env.ref('base.res_partner_1').id,
            'pricelist_id': cls.pricelist.id,
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
            'recurring_invoice': False,
        })
        cls.product_one_time = cls.env['product.product'].create({
            'name': 'Recurring Consumable',
            'recurring_invoice': True,
            'type': 'consu',
            'list_price': 200.0,
            'accept_one_time': True,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6.0}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16.0}),
            ],
        })
        cls.subscription_product = cls.env['product.product'].create({
            'name': 'Recurring Consumable',
            'recurring_invoice': True,
            'type': 'consu',
            'list_price': 200.0,
            'product_subscription_pricing_ids': [
                Command.create({'plan_id': cls.plan_monthly.id, 'price': 6.0}),
                Command.create({'plan_id': cls.plan_yearly.id, 'price': 16.0}),
            ],
        })
