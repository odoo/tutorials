from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    division_price = fields.Float(string="Division")
    division_price_tags = fields.Many2many('sale.order.line.tag', string="Division Tags", compute='_compute_divided_price_tags', store=True)
    parent_division_id = fields.Many2one('sale.order.line')

    @api.depends('division_price', 'parent_division_id')
    def _compute_divided_price_tags(self):
        for line in self:
            tags = []
            if not line.parent_division_id:
                rounded_price = round(line.division_price, 2)
                tag = self.env['sale.order.line.tag'].create({
                    'name': f"{rounded_price}",
                    'color': 1,
                })
                tags.append(tag.id)
            else:
                color_index = hash(line.parent_division_id.id) % 10
                tag = self.env['sale.order.line.tag'].create({
                    'name': f"{line.division_price}",
                    'color': color_index,
                })
                tags.append(tag.id)
            line.division_price_tags = [(6, 0, tags)]
