from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_modular_types = fields.Boolean(compute="_compute_has_modular_types", store=True)
    is_modular_type_set = fields.Boolean()

    @api.depends("product_id.modular_type_ids")
    def _compute_has_modular_types(self):
        for line in self:
            line.has_modular_types = bool(line.product_id.modular_type_ids)
