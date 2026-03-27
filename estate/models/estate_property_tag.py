from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char('Tags', required=True)
    color = fields.Integer()

    _check_tag_name = models.Constraint("UNIQUE(name)", "Property tag name must be unique")
