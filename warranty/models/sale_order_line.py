from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    warranty_line_id = fields.Many2one('sale.order.line', string="Warranty")
    warranty_line_ids = fields.One2many('sale.order.line', 'warranty_line_id', string="Warranty")
