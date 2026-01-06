from odoo import fields, models


class SaleOrderLineModularValue(models.Model):
    _name = 'sale.order.line.modular.value'
    _description = 'Sale order line modular value'

    order_line_id = fields.Many2one('sale.order.line')
    modular_type_id = fields.Many2one('modular.type')
    value = fields.Float()
