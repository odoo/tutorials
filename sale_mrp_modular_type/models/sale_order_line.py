from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    has_modular_type = fields.Boolean(
        compute='_compute_has_modular_type', store=True
    )
    modular_value_ids = fields.One2many(
        'sale.order.line.modular.value', 'order_line_id'
    )

    @api.depends('product_template_id', 'product_template_id.modular_type_ids')
    def _compute_has_modular_type(self):
        for line in self:
            line.has_modular_type = bool(
                line.product_template_id.modular_type_ids
            )

    def _set_default_modular_values(self):
        vals_list = []
        for line in self:
            existing_types = line.modular_value_ids.mapped('modular_type_id')
            missing_types = line.product_template_id.modular_type_ids - existing_types
            for modular_type in missing_types:
                vals_list.append({
                    'order_line_id': line.id,
                    'modular_type_id': modular_type.id,
                    'value': 0.0,
                })
        if vals_list:
            self.env['sale.order.line.modular.value'].create(vals_list)
