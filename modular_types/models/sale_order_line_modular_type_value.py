from odoo import models, fields


class SaleOrderLineModularValue(models.Model):
    _name = 'sale.order.line.modular.value'

    order_line_id = fields.Many2one('sale.order.line', ondelete='cascade')
    modular_type_id = fields.Many2one('modular.type', required=True)
    value = fields.Float()
