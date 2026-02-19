from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag describing a particular property characteristic"
    _check_name = models.Constraint('UNIQUE(name)', 'A tag with this name already exists')
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()
