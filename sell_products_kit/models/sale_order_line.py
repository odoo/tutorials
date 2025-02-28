from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(related="product_id.is_kit")
    parent_line_id = fields.Many2one("sale.order.line", ondelete="cascade")
    sub_product_ids = fields.Many2many(
        "product.product",
        related="product_template_id.sub_product_ids",
        string="Sub Products",
    )
    last_price = fields.Float(
        string="Last Price", help="Stores the last price before setting it to 0"
    )

    def action_open_kit_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Sub Products",
            "view_mode": "form",
            "res_model": "sub.product.wizard",
            "target": "new",
        }
