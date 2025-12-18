from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    name = fields.Char(required=True)
    _name_unique = models.Constraint("unique(name)", "Type must be unique")
