from odoo import fields, models


# model for reffer tags
class DividedCostTag(models.Model):
    _name = 'divided.cost.tag'
    _description = 'Divided Cost Tag'

    name = fields.Char(string="Division Tag")
    color = fields.Integer(string="color")
