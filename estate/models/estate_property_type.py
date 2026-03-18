from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

    _check_name = models.Constraint("UNIQUE(name)", "Name must be unique.")
