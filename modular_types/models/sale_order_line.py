from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_modular_type = fields.Boolean(compute='_compute_has_modular_type', store=True)
    modular_value_ids = fields.One2many('sale.order.line.modular.value', 'order_line_id')

    @api.depends('product_template_id', 'product_template_id.modular_types')
    def _compute_has_modular_type(self):
        for line in self:
            line.has_modular_type = bool(
                line.product_template_id.modular_types
            )
