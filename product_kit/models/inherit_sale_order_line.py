from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_kit = fields.Boolean(compute="_compute_product_is_kit")
    parent_id = fields.Many2one('sale.order.line', ondelete='cascade')
    kit_price = fields.Float()

    @api.depends('product_id.is_kit')
    def _compute_product_is_kit(self):
        for records in self:
            records.is_kit = records.product_id.is_kit

    def write(self, values):
        if 'parent_id' in values or self.parent_id:
            return False
        return super(SaleOrderLine, self).write(values)
