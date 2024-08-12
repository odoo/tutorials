from odoo import models, fields


class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "estate property tag description"
    _order = "name"

    name = fields.Char('Name', required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)',
         "A tag with the same name already exists")
    ]
    color = fields.Integer("Color")
