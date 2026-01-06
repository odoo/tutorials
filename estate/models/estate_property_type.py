from odoo import fields, models


class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "this is property model"

    name = fields.Char("home.plan", required=True)

    _check_unique_propertyType = models.Constraint(
        "UNIQUE(name)", "The Property type must be unique"
    )
