from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestConfirmSaleOrder(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.manager_group = cls.env.ref("sales_team.group_sale_manager")
        cls.user_group = cls.env.ref("sales_team.group_sale_salesman")

        cls.manager_user = cls.env["res.users"].create({
            "name": "Manager User",
            "login": "manager@example.com",
            "groups_id": [(6, 0, [cls.manager_group.id])]
        })

        cls.salesperson_user = cls.env["res.users"].create({
            "name": "Salesperson User",
            "login": "salesperson@example.com",
            "groups_id": [(6, 0, [cls.user_group.id])]
        })

        cls.product = cls.env["product.template"].create({
            "name": "Test Product",
            "type": "consu",  
            "qty_available": 5,  
        })
        
        cls.sale_order = cls.env["sale.order"].create({
            "partner_id": cls.env["res.partner"].create({"name": "Test Partner"}).id,
            "user_id": cls.salesperson_user.id,
        })

        cls.sale_order_line = cls.env["sale.order.line"].create({
            "name": cls.product.name, 
            "order_id": cls.sale_order.id,
            "product_id": cls.product.product_variant_id.id,
            "product_uom_qty": 10, 
        })

    def test_confirm_order_insufficient_stock_without_approval(self):
        self.sale_order = self.sale_order.with_user(self.salesperson_user)
        with self.assertRaises(UserError, msg="You cannot confirm order if any ordered product has insufficient stock."):
            self.sale_order.action_confirm()

    def test_confirm_order_insufficient_stock_with_approval(self):
        self.sale_order = self.sale_order.with_user(self.salesperson_user)
        self.sale_order.zero_stock_approval = True  
        self.sale_order.action_confirm() 
        self.assertEqual(self.sale_order.state, "sale", "Order should be confirmed when zero stock approval is granted.")

    def test_manager_can_approve_zero_stock(self):
        self.sale_order = self.sale_order.with_user(self.manager_user)
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, "sale", "Manager should be able to approve and confirm zero stock order.")
