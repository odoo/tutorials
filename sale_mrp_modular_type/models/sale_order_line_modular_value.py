from odoo import fields, models


class SaleOrderLineModularValue(models.Model):
    _name = 'sale.order.line.modular.value'
    _description = 'Sale Order Line Modular Value'

    order_line_id = fields.Many2one(
        'sale.order.line', required=True, ondelete='cascade'
    )
    modular_type_id = fields.Many2one('modular.type', required=True)
    value = fields.Float(help="Quantity multiplier")
