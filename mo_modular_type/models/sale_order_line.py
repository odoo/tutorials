from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    has_modular_types = fields.Boolean(
        string="Has modular type", compute="_compute_has_modular_types"
    )
    modular_type_values = fields.One2many('sale.order.line.modular.value', 'order_line_id', string="Modular Type Values")

    @api.depends("product_id")
    def _compute_has_modular_types(self):
        for record in self:
            record.has_modular_types = bool(record.product_id.modular_types)


class SaleOrderLineModularValue(models.Model):
    _name = 'sale.order.line.modular.value'
    _description = 'Sales Order Line Modular Value'

    order_line_id = fields.Many2one('sale.order.line', required=True, ondelete='cascade')
    modular_type_id = fields.Many2one('module.types', string="Modular Type", required=True)
    value = fields.Float(string="Value", required=True)
