# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, _, api, fields, models


class SaleOrderWarranty(models.TransientModel):
    _name = "sale.order.warranty"
    _description = "Warranty Wizard"

    sale_order_id = fields.Many2one(comodel_name="sale.order", required=True, ondelete="cascade")
    wizard_line_ids = fields.One2many(comodel_name="sale.order.warranty.line", inverse_name="wizard_id")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        sale_order_id = self.env.context.get("active_id")
        sale_order_lines = self.env["sale.order"].browse(sale_order_id).order_line
        wizard_line_values = []
        for line in sale_order_lines:
            if line.product_id.is_warranty_available and not line.warranty_line_ids:
                wizard_line_values.append({"order_line_id": line.id, "product_id": line.product_id.id})
        res["wizard_line_ids"] = [Command.clear()] + [Command.create(vals) for vals in wizard_line_values]
        res["sale_order_id"] = sale_order_id
        return res

    def action_add_warranty(self):
        order_lines = []
        for warranty_line in self.wizard_line_ids:
            if not warranty_line.product_warranty_id:
                continue
            order_lines.append({
                'order_id': self.sale_order_id.id,
                'product_id': warranty_line.product_warranty_id.product_id.id,
                'price_unit': warranty_line.order_line_id.price_unit * warranty_line.product_warranty_id.percent / 100,
                'name': _(f"Extended Warranty\nWarranty For Product: {warranty_line.order_line_id.product_id.name}\nEnd Date: {warranty_line.end_date}"),
                'warranty_parent_line_id': warranty_line.order_line_id.id
            })
        if len(order_lines) > 0:
            self.env['sale.order.line'].create(order_lines)


class SaleOrderWarrantyLine(models.TransientModel):
    _name = "sale.order.warranty.line"
    _description = "Warranty Wizard Line"

    wizard_id = fields.Many2one(comodel_name="sale.order.warranty", required=True, ondelete="cascade")
    order_line_id = fields.Many2one(comodel_name="sale.order.line", required=True, ondelete="cascade")
    product_id = fields.Many2one(comodel_name="product.product")
    product_warranty_id = fields.Many2one(comodel_name="product.warranty")
    end_date = fields.Date(string="Warranty End Date", compute="_compute_end_date")

    @api.depends("product_warranty_id")
    def _compute_end_date(self):
        for record in self:
            if record.product_warranty_id:
                record.end_date = fields.Date.add(
                    fields.Date.context_today(record=record),
                    years=record.product_warranty_id.duration
                )
            else:
                record.end_date = None
