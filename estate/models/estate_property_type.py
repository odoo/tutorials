from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"

    name = fields.Char("Type Name", required=True)

    # Constraints
    _unique_name = models.Constraint("UNIQUE(name)", "Property Type name must unique!")
