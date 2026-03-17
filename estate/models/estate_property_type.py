from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Property Type"

    name = fields.Char("Property Type", required=True)

    _check_type_name = models.Constraint("UNIQUE(name)", "Property type name must be unique")
