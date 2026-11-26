from odoo.tests import TransactionCase, tagged
from odoo.exceptions import AccessError, UserError
from odoo.fields import Command


@tagged('post_install', '-at_install', 'nice')
class TestSaleOrder(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group_sale_salesman = cls.env.ref('sales_team.group_sale_salesman')
        cls.group_sale_manager = cls.env.ref('sales_team.group_sale_manager')
        cls.group_sale_order_approval_user = cls.env.ref('sale_order.sale_order_approval_group')

        cls.sale_user = cls.env['res.users'].create({
            'name': 'Test Salesman',
            'login': 'salesman',
            'password': 'salesman',
            'email': 'default_user_salesman@example.com',
            'notification_type': 'email',
            'group_ids': [
                Command.set(cls.group_sale_salesman.ids)
            ],
        })
        cls.sale_manager = cls.env['res.users'].create({
            'name': 'Test Sales Manager',
            'login': 'salesmanager',
            'password': 'salesmanager',
            'email': 'default_user_salesmanager@example.com',
            'notification_type': 'email',
            'group_ids': [
                Command.set(cls.group_sale_manager.ids)
            ],
        })
        cls.sale_order_approved_user = cls.env['res.users'].create({
            'name': 'Test Sale Order Approved User',
            'login': 'salesorderman',
            'password': 'saleorderman',
            'email': 'default_user_salesorderman@example.com',
            'notification_type': 'email',
            'group_ids': [
                Command.link(cls.group_sale_salesman.id),
                Command.link(cls.group_sale_order_approval_user.id),
            ],
        })

        cls.product = cls.env['product.product'].create({
            'name': 'test-product',
            'is_storable': True
        })

        cls.partner1, cls.partner2 = cls.env['res.partner'].create([
            {'name': 'Partner 1'},
            {'name': 'Partner 2'},
        ])

    def setUp(self):
        self.order = self.env['sale.order'].with_user(self.sale_user).create({
            'partner_id': self.partner1.id,
        })

        self.order_with_line_without_approval = self.env['sale.order'].with_user(self.sale_user).create({
            'partner_id': self.partner2.id,
            'order_line': [
                Command.create({
                    'product_id': self.product.id,
                    'product_uom_qty': 10
                })
            ],
            'zero_stock_approval': False
        })

        self.order_with_line_with_approval = self.env['sale.order'].with_user(self.sale_user).create({
            'partner_id': self.partner2.id,
            'order_line': [
                Command.create({
                    'product_id': self.product.id,
                    'product_uom_qty': 10
                })
            ],
            'zero_stock_approval': True
        })

    def test_create_user(self):
        self.assertTrue(self.sale_user and self.sale_manager and self.sale_order_approved_user)

    def test_order_without_order_line(self):
        with self.assertRaises(UserError):
            self.order.action_confirm()

    def test_sale_user_without_approval(self):
        with self.assertRaises(UserError):
            self.order_with_line_without_approval.action_confirm()

    def test_sale_user_with_approval(self):
        self.assertTrue(
            self.order_with_line_with_approval.action_confirm()
        )

    def test_sale_manager_without_approval(self):
        order = self.order_with_line_without_approval.with_user(self.sale_manager)

        with self.assertRaises(UserError):
            order.action_confirm()

    def test_sale_manager_with_approval(self):
        order = self.order_with_line_with_approval.with_user(self.sale_manager)

        self.assertTrue(order.action_confirm())

    def test_sale_user_change_approval_field(self):
        with self.assertRaises(AccessError):
            self.order_with_line_without_approval.write({
                'zero_stock_approval': True
            })

    def test_sale_approved_user_change_approval_field(self):
        self.order_with_line_approval_user = self.env['sale.order'].with_user(self.sale_order_approved_user).create(
            {
                'partner_id': self.partner2.id,
                'order_line': [
                    Command.create({
                        'product_id': self.product.id,
                        'product_uom_qty': 10,
                    })
                ],
                'zero_stock_approval': False,
            })

        self.assertTrue(
            self.order_with_line_approval_user.write({
                'zero_stock_approval': True
            })
        )
