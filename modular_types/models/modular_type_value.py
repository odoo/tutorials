from odoo import fields, models


class ModularTypeValue(models.Model):
    _name = 'modular.type.value'
    _description = 'Modular Type Value for Sale Order Line'

    sale_order_line_id = fields.Many2one(
        'sale.order.line', string='Sale Order Line', ondelete='cascade'
    )
    modular_type_id = fields.Many2one(
        comodel_name='product.modular.type',
        string='Modular Type',
        required=True,
        ondelete='cascade',
    )
    value = fields.Float('Value', required=True)
