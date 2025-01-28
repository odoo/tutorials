from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char('Property Tag', required=True, translate=True)
    color = fields.Integer(string="Color")  # Add the color field

    property_ids = fields.Many2many('estate_property', string="Properties")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]
   