from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    divided_price = fields.Float(string="Division", default="0.0")
    divided_price_tags = fields.Many2many('sale.order.line.tag', string="Division", compute='_compute_divided_price_tags', store=True)
    parent_division_id = fields.Many2one('sale.order.line')
    unit_price = fields.Float(string="Unit Price", compute="_compute_unit_price")

    @api.depends("price_subtotal", "product_uom_qty")
    def _compute_unit_price(self):
        for line in self:
            line.unit_price = line.price_subtotal / line.product_uom_qty

    @api.depends('divided_price', 'parent_division_id')
    def _compute_divided_price_tags(self):
        for line in self:
            tags = []
            if not line.parent_division_id:
                rounded_price = round(line.divided_price, 2)
                tag = self.env['sale.order.line.tag'].create({
                    'name': f"{rounded_price}",
                    'color': 1,
                })
                tags.append(tag.id)
            else:
                color_index = hash(line.parent_division_id.id) % 10
                tag = self.env['sale.order.line.tag'].create({
                    'name': f"{line.divided_price}",
                    'color': color_index,
                })
                tags.append(tag.id)
            line.divided_price_tags = [(6, 0, tags)]

    def action_distribute_cost(self):
        order = self.order_id
        total_price = self.price_subtotal
        return {
            'type': 'ir.actions.act_window',
            'name': 'Distribute Cost',
            'res_model': 'distribute.cost.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': order.id,        
                'original_total_price': total_price,
            },
        }
    
    def unlink(self):
        for line in self:
            if not line.parent_division_id.id:
                child_lines = self.env['sale.order.line'].search([('parent_division_id', '=', line.id)])
                for child in child_lines:
                    child.price_subtotal = child.price_subtotal - child.divided_price
                    child.divided_price = 0.0
            elif line.parent_division_id.id:
                child_lines = self.env['sale.order.line'].search([('parent_division_id', '=', line.id)])
                parent_line = line.parent_division_id
                if child_lines:        
                    for child in child_lines:
                        child.price_subtotal -= (line.price_unit * line.product_uom_qty) / len(child_lines)
                        child.divided_price = 0.0
                        child.parent_division_id = None
                if parent_line:
                    parent_line.price_subtotal += line.price_subtotal
                line.divided_price = 0.0
                line.parent_division_id = None
            else:
                line.parent_division_id.divided_price += line.divided_price
        return super().unlink()
    
class SaleOrderLineTag(models.Model):
    _name = 'sale.order.line.tag'
    _description = 'Sale Order Line Tag'

    name = fields.Char(string="Tag Name")
    color = fields.Integer(string="Tag Color", default='grey')
