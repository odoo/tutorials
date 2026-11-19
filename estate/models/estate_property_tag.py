from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for estate properties"

    name = fields.Char('Name', required=True, translate=True)

    _unique_name = models.Constraint('UNIQUE(name)', 'Tag name must be unique.')
