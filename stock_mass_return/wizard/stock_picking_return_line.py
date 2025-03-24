# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain="[('id', 'in', allowed_product_ids)]",
    )
    allowed_product_ids = fields.Many2many(
        "product.product",
        string="Allowed Products",
        related="wizard_id.allowed_product_ids",
        store=False,
    )
    allowed_picking_ids = fields.Many2many("stock.picking")
    picking_id = fields.Many2one(
        "stock.picking",
        string="Sale Order",
        domain="[('id', 'in', allowed_picking_ids)]",
    )
    allowed_sale_order_ids = fields.Many2many("sale.order")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order", domain="[('id', 'in', allowed_sale_order_ids)]",)
    allowed_purchase_order_ids = fields.Many2many("purchase.order")
    purchase_order_id = fields.Many2one("purchase.order", string="Purchase Order", domain="[('id', 'in', allowed_purchase_order_ids)]",)

    @api.onchange("purchase_order_id")
    def _onchange_purchase_order_id(self):
        if self.purchase_order_id:
            self.picking_id = self.env["stock.picking"].search(
                [("id", "in", self.purchase_order_id.picking_ids.ids)], limit=1
            )

    @api.onchange("sale_order_id")
    def _onchange_sale_order_id(self):
        if self.sale_order_id:
            self.picking_id = self.wizard_id.picking_ids.filtered(
                lambda p: p.sale_id == self.sale_order_id._origin
            )

    @api.onchange("product_id","picking_id")
    def _onchange_product_id_and_picking_id(self):
        if self.product_id:
            move = self.picking_id.move_ids.filtered(lambda m: m.product_id == self.product_id)
            self.move_id = move.id

            self.allowed_picking_ids = self.wizard_id.picking_ids.filtered(
                lambda p: p.move_ids.filtered(
                    lambda m: m.product_id == self.product_id
                )
            ).ids

            if self.wizard_id.picking_type_id.code == "outgoing":
                allowed_sales = [
                    picking.sale_id.id
                    for picking in self.allowed_picking_ids
                    if picking.sale_id
                ]
                self.allowed_sale_order_ids = [(6, 0, allowed_sales)]
            else:
                allowed_purchase = self.env["purchase.order"].search([
                        ("picking_ids", "in", self.allowed_picking_ids.ids),
                        ("order_line.product_id", "=", self.product_id.id),
                    ])
                self.allowed_purchase_order_ids = [(6, 0, allowed_purchase.ids)]

            if (self.allowed_purchase_order_ids and len(self.allowed_purchase_order_ids) == 1):
                self.purchase_order_id = self.allowed_purchase_order_ids[0].id

            if self.allowed_sale_order_ids and len(self.allowed_sale_order_ids) == 1:
                self.sale_order_id = self.allowed_sale_order_ids[0].id

            if len(self.allowed_picking_ids) == 1:
                self.update({"picking_id": self.allowed_picking_ids[0]})
