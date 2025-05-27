# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, Command, fields, models


class ProductWarrantyWizard(models.TransientModel):
    _name = "product.warranty.wizard"
    _description = "product warranty wizard"

    wizard_line_ids = fields.One2many(
        "product.warranty.wizard.line", "warranty_wizard_id"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_order = self.env["sale.order"].browse(self._context.get("active_id"))
        product_lines = active_order.order_line.filtered(
            lambda line: not line.is_warranty and line.product_id.has_warranty
        )
        res["wizard_line_ids"] = [
            Command.create(
                {
                    "order_line_id": line.id,
                    "product_id": line.product_id.id,
                    "warranty_product_id": (
                        line.warranty_product_id.id if line.warranty else False
                    ),
                }
            )
            for line in product_lines
        ]
        return res

    def add_warranty(self):
        self.ensure_one()
        order_id = self.env.context.get("active_id")
        for line in self.wizard_line_ids:
            if not line.warranty_product_id:
                continue
            existing_warranty = self.env["sale.order.line"].search(
                [
                    ("order_id", "=", order_id),
                    ("is_warranty", "=", True),
                    ("products", "=", line.order_line_id.id),
                    ("warranty_product_id", "=", line.warranty_product_id.id),
                ],
                limit=1,
            )
            if existing_warranty:
                continue
            if line.order_line_id.warranty:
                self._update_existing_warranty(line)
            else:
                self._create_new_warranty(line, order_id)

    def _update_existing_warranty(self, line):
        line.order_line_id.warranty_orderline.write(
            {
                "product_id": line.warranty_product_id.product_id.id,
                "name": f"{line.warranty_product_id.name} End Date: {line.warranty_end_date}",
                "price_unit": (
                    line.order_line_id.price_unit
                    * (line.warranty_product_id.percentage / 100)
                ),
            }
        )
        line.order_line_id.warranty_product_id = line.warranty_product_id.id

    def _create_new_warranty(self, line, order_id):
        warranty_order_line = self.env["sale.order.line"].create(
            {
                "order_id": order_id,
                "product_id": line.warranty_product_id.product_id.id,
                "name": f"{line.warranty_product_id.name} End Date: {line.warranty_end_date}",
                "product_uom_qty": 1,
                "price_unit": (
                    line.order_line_id.price_unit
                    * (line.warranty_product_id.percentage / 100)
                ),
                "is_warranty": True,
                "products": line.order_line_id.id,
                "sequence": line.order_line_id.sequence + 1,
            }
        )
        line.order_line_id.write(
            {
                "warranty": True,
                "warranty_product_id": line.warranty_product_id.id,
                "warranty_orderline": warranty_order_line,
            }
        )
