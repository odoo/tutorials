from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _type_unique = models.Constraint("unique(name)", "Name already Exist")

    name = fields.Char(required=True)
