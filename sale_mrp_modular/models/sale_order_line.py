from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    modular_value_ids = fields.One2many('sale.mrp.modular.wizard.line', 'source_sale_order_line_id', string='Modular Values')
