from odoo import api, fields, models
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_kit = fields.Boolean(compute="_compute_is_kit")
    parent_product_id = fields.Many2one('product.product')
    is_subproduct = fields.Boolean(default=False)

    @api.depends('product_template_id')
    def _compute_is_kit(self):
        for line in self:
            line.is_kit = line.product_template_id.is_kit

    def unlink(self):

        sub_products = self.search([('parent_product_id', '=', self.product_id.id)])

        for sub_product in sub_products:
            sub_product.unlink()

        return super(SaleOrderLine, self).unlink()
