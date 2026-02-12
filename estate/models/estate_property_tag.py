from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _tags_unique = models.Constraint("unique(name)", "Name already exist")
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()
