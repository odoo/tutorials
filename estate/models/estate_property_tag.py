from odoo import fields, models


class Tag(models.Model):
    _name = "estate.property.tag"
    _description = "Propert tag"
    _name_uniq = models.Constraint('unique(name)', 'A tag with the same name allready exist')

    name = fields.Char(required=True)
