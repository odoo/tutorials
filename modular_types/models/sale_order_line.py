from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_modular_type = fields.Boolean(compute='_compute_has_modular_type', store=True)
    modular_type_value_ids = fields.One2many('modular.type.value', 'sale_order_line_id')

    @api.depends('product_id')
    def _compute_has_modular_type(self):
        for line in self:
            line.has_modular_type = (
                bool(line.product_id.product_tmpl_id.modular_type_ids)
                if line.product_id
                else False
            )
