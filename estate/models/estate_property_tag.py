from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"

    name = fields.Char("Tag Name", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The name of the Tag should be unique')
    ]
