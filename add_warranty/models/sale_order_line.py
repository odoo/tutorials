from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    warranty_item = fields.Many2one(
        comodel_name='warranty.configuration',
        string="Warranty",
        default=None)

    end_date = fields.Date(string="Expiry Date")

    related_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string="Related Product Line",
        help="The original product line this warranty is linked to",
        ondelete='cascade')
    
    @api.onchange("warranty_item")
    def _onchange_warranty_product(self):
        num_year = self.warranty_item.period
        self.end_date = fields.Date.today() + relativedelta(years=num_year)

    def unlink(self):
        if self.warranty_item.id is False and self.related_line_id.id:
            corresponding_product_line = self.env['sale.order.line'].search([
                ('id','=',self.related_line_id.id)
            ])
            corresponding_product_line.warranty_item = False
            corresponding_product_line.end_date = False
        else:
            warranty_lines = self.env['sale.order.line'].search([
                ('related_line_id', 'in', self.ids)
            ])
            if warranty_lines:
                warranty_lines.unlink()
        return super(SaleOrderLine, self).unlink()
