from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "property tags"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _unique_tag = models.Constraint("unique(name)", "This tag already exists")
