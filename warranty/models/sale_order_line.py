from odoo import models, fields
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    warranty_line_id = fields.Many2one(
        string="Warranty Line",
        comodel_name="sale.order.line",
        ondelete="cascade",
        domain="[('order_id', '=', order_id)]",
        copy=False,
        index=True,
    )
    warranty_line_ids = fields.One2many(
        string="Warranty Lines",
        comodel_name="sale.order.line",
        inverse_name="warranty_line_id",
    )



