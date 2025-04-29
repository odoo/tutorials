from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(compute='_compute_is_kit', store=True)
    parent_kit_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Parent Kit Line',
        ondelete='cascade',
        index=True,
    )

    # Optional fields for sub-products
    sub_product_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='parent_kit_line_id',
        string='Sub Product Lines',
        copy=True,
    )
    custom_sub_product_price = fields.Float(
        string='Custom Sub Product Price',
        help='Overridden price of the sub product line.',
    )

    @api.depends('product_id')
    def _compute_is_kit(self):
        for line in self:
            line.is_kit = line.product_id.is_kit if line.product_id else False
