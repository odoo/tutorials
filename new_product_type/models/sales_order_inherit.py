from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit_product = fields.Boolean(string="Is Kit Product", compute="_compute_is_kit", store=True)
    kit_component_ids = fields.One2many("sale.order.line", "parent_line_id", string="Kit Components")
    parent_line_id = fields.Many2one("sale.order.line", string="Parent Kit Line", ondelete="cascade")
    display_price_unit = fields.Float(compute="_compute_display_price_unit", readonly=False)
    display_price_subtotal = fields.Float(compute="_compute_display_price_subtotal")

    @api.depends("product_id")
    def _compute_is_kit(self):
        for line in self:
            line.is_kit_product = line.product_id.product_tmpl_id.is_kit

    def _compute_display_price_unit(self):
        for line in self:
            if line.parent_line_id:
                line.display_price_unit = 0.0
            else:
                line.display_price_unit = line.price_unit

    def _compute_display_price_subtotal(self):
        for line in self:
            if line.parent_line_id:
                line.display_price_subtotal = 0.0
            else:
                line.display_price_subtotal = line.price_subtotal

    def action_open_kit_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Kit Wizard",
            "res_model": "kit.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_sale_order_line_id": self.id},
        }