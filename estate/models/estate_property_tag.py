from odoo import fields, models


class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate tag"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_offer_price = models.Constraint(
        "unique(name)",
        "A tag with the same name already exists",
    )
