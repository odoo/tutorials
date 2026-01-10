from odoo import api, fields, models


class saleOrderLine(models.Model):
    _inherit = "sale.order.line"

    modular_type_value_ids = fields.One2many(
        "sale.order.line.modular.type", "order_line_id", string="Modular Type Value"
    )

    is_modular_types = fields.Boolean(
        string="Has modular type", compute="_compute_has_modular_types"
    )

    @api.depends("product_template_id")
    def _compute_has_modular_types(self):
        for record in self:
            record.is_modular_types = bool(record.product_template_id.modular_type_ids)
