from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(
        string="Name",
        help="The name of the property type.",
        required=True
    )
