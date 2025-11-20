from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "property tag"

    name = fields.Char(required=True)

    _check_name = models.Constraint('UNIQUE(name)', 'The tag name must be unique')
