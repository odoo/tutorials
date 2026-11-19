from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    # region constraints
    _unique_name = models.Constraint(
        "UNIQUE(name)", "The property type name must be unique"
    )
    # endregion
