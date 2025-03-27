from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    division_price = fields.Float(string="Division Price")
    division_price_tags = fields.Many2many('sale.order.line.tag', string="Division", compute='_compute_division_price_tags', store=True)
    distributed_line = fields.Many2one('sale.order.line')

    @api.depends('division_price', 'distributed_line')
    def _compute_division_price_tags(self):
        for line in self:
            tags = []
            if not line.distributed_line:
                rounded_price = round(line.division_price, 2)
                tag = self.env['sale.order.line.tag'].create({
                    'name': f"{rounded_price}",
                    'color': 1,
                })
                tags.append(tag.id)
            else:
                color_index = hash(line.distributed_line.id) % 10
                tag = self.env['sale.order.line.tag'].create({
                    'name': f"{line.division_price}",
                    'color': color_index,
                })
                tags.append(tag.id)
            if line.division_price == 0.0:
               line.division_price_tags = [(5, 0, 0)]
            else:
               line.division_price_tags = [(6, 0, tags)]

    def unlink(self):
        for line in self:
            if not line.distributed_line.id:
                divided_lines = self.env['sale.order.line'].search([('distributed_line', '=', line.id)])
                for line in divided_lines:
                    line.price_subtotal = line.price_subtotal - line.division_price
                    line.division_price = 0.0
            elif line.distributed_line.id:
                divided_lines = self.env['sale.order.line'].search([('distributed_line', '=', line.id)])
                if divided_lines:
                    for line in divided_lines:
                        line.price_subtotal -= (line.price_unit * line.product_uom_qty) / len(divided_lines)
                        if(line.price_subtotal<0):
                            raise ValidationError("You cannot delete this as Amount will be negative")
                        line.division_price = 0.0
                        line.distributed_line = None
                if line.distributed_line:
                    line.distributed_line.price_subtotal += (line.price_subtotal - (line.product_uom_qty*line.price_unit))
                    if(line.distributed_line.price_subtotal<0):
                            raise ValidationError("You cannot delete this as Amount will be negative")
            else:
                line.distributed_line.division_price += line.division_price
        return super().unlink()
