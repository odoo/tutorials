from odoo import api,models,fields,Command


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    parent_line_id = fields.Many2one(comodel_name='sale.order.line', ondelete="cascade")
    is_kit = fields.Boolean(related='product_template_id.is_kit', store=True)

    def unlink(self):
        for line in self:
            if line.product_id.is_kit:
                line.order_id.order_line.filtered(lambda l: l.parent_line_id == line).unlink()
        return super().unlink()

    def write(self, vals):
        if(vals.get('product_template_id')):
            product_template = self.env['product.template'].browse(vals.get('product_template_id'))
            vals['price_unit'] = product_template.list_price 
            self.search([('parent_line_id', '=', self.id)]).unlink()
        return super().write(vals)
