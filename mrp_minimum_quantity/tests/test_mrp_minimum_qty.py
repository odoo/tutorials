from odoo import Command, _
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged, TransactionCase
from odoo.tools import mute_logger
from psycopg2 import IntegrityError


@tagged("post_install", "-at_install")
class TestMrpMinimumQty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user = cls.env.ref("base.user_admin")
        cls.normal_user = cls.env["res.users"].create({
            "name": "Normal User",
            "login": "normal_user",
            "groups_id": [Command.link(cls.env.ref("mrp.group_mrp_user").id)]
        })
        cls.mrp_admin_user = cls.env["res.users"].create({
            "name": "MRP Admin",
            "login": "mrp_admin",
            "groups_id": [
                    Command.link(cls.env.ref("mrp.group_mrp_manager").id),
                    Command.link(cls.env.ref("stock.group_stock_manager").id)
            ],
        })
        cls.vendor = cls.env["res.partner"].create({
            "name": "Test Vendor",
        })
        cls.product = cls.env["product.product"].create({
            "name": "Test Product",
            "type": "consu",
            "route_ids": [Command.link(cls.env.ref("mrp.route_warehouse0_manufacture").id)]
        })
        cls.bom = cls.env["mrp.bom"].create({
            "product_tmpl_id": cls.product.product_tmpl_id.id,
            "product_qty": 10,
            "product_min_qty": 5
        })
        cls.env.ref("stock.route_warehouse0_mto").action_unarchive()
        cls.mto_product = cls.env["product.product"].create({
            "name": "MTO Product",
            "type": "consu",
            "route_ids": [
                Command.link(cls.env.ref("stock.route_warehouse0_mto").id),
                Command.link(cls.env.ref("purchase_stock.route_warehouse0_buy").id)
            ],
            "seller_ids": [Command.create({"partner_id": cls.vendor.id, "price": 100.0})],
        })
        cls.sale_order = cls.env["sale.order"].create({
            "partner_id": cls.env.ref("base.res_partner_1").id
        })
        cls.sale_order_line = cls.env["sale.order.line"].create({
            "order_id": cls.sale_order.id,
            "product_id": cls.mto_product.id,
            "product_uom_qty": 5,
            "price_unit": 150.0
        })

    @mute_logger("odoo.sql_db")
    def test_quantity_greater_than_minimum(self):
        with self.assertRaises(IntegrityError):
            self.bom.update({"product_qty": 4})

    def test_mrp_order_quantity_validation(self):
        mo = self.env["mrp.production"].with_user(self.normal_user.id).create({
            "product_id": self.product.id,
            "product_qty": 4,
            "bom_id": self.bom.id
        })
        with self.assertRaises(ValidationError):
            mo._onchange_product_qty()
        mo_admin = self.env["mrp.production"].with_user(self.mrp_admin_user.id).create({
            "product_id": self.product.id,
            "product_qty": 4,
            "bom_id": self.bom.id
        })
        self.assertEqual(mo_admin._onchange_product_qty()["warning"]["title"], _("Warning"))

    def test_replenishment_validation(self):
        manufacture_route = self.env.ref("mrp.route_warehouse0_manufacture")
        self.orderpoint = self.env["stock.warehouse.orderpoint"].create({
            "product_id": self.product.id,
            "qty_to_order": 4,
            "trigger": "manual",
            "route_id": manufacture_route.id
        })
        with self.assertRaises(UserError):
            self.orderpoint.with_user(self.normal_user.id).action_replenish()
        self.orderpoint.with_user(self.mrp_admin_user.id).action_replenish()
        self.env["stock.warehouse.orderpoint"].search([("product_id", "=", self.product.id)]).unlink()
        self.env["mrp.production"].search([("state", "!=", "done")]).unlink()
        self.orderpoint = self.env["stock.warehouse.orderpoint"].create({
            "product_id": self.product.id,
            "qty_to_order": 4,
            "trigger": "auto",
            "route_id": manufacture_route.id
        })
        self.orderpoint.sudo().action_replenish_auto()
        mo = self.env["mrp.production"].search([], order="id desc", limit=1)
        self.assertTrue(mo)
        self.assertEqual(mo.product_qty, 5.0)

    def test_mto_price_transfer_to_po(self):
        self.sale_order.sudo().action_confirm()
        purchase_order = self.env["purchase.order"].search([("origin", "=", self.sale_order.name)], limit=1)
        self.assertTrue(purchase_order)
        purchase_order_line = self.env["purchase.order.line"].search([
            ("order_id", "=", purchase_order.id),
            ("product_id", "=", self.mto_product.id)], limit=1)
        self.assertTrue(purchase_order_line)
        self.assertEqual(purchase_order_line.price_unit, self.sale_order_line.price_unit)
