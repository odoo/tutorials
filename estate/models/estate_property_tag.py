from odoo import fields, models


class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "this is property tag model"

    name = fields.Char("home.plan", required=True)
    _check_unique_propertyTag = models.Constraint(
        "UNIQUE(name)", "The Property tag must be unique"
    )
