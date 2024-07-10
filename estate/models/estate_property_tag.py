from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Properties Tag defined"

    # order
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")

    # sql constraints
    _sql_constraints = [('name_unique', 'unique(name)', "Tag Name should be unique")]
