from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char('Tag', required=True)

    _check_name = models.Constraint("UNIQUE(name)", "Tag name must be unique.")
