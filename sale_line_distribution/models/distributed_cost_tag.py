from odoo import fields, models


class DistributedCostTag(models.Model):
    _name = 'distributed.cost.tag'
    _description = 'Distributed Cost Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color index")
    sale_order_line = fields.Many2one(comodel_name='sale.order.line', string="Order Line")
    parent_tag = fields.Many2one(comodel_name='distributed.cost.tag', string="Parent Tag")
    child_tags = fields.One2many(comodel_name='distributed.cost.tag', string="Child Tag", inverse_name='parent_tag')