from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _name_unique = models.Constraint('UNIQUE(name)', 'Tag name must be unique.')
