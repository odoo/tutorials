from odoo import fields, models


class Type(models.Model):
    _name = "estate.property.type"
    _description = "Property type"
    _name_uniq = models.Constraint('unique(name)', 'This property type allready exist')

    name = fields.Char(required=True)
