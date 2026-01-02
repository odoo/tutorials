from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate_type"
    _description = "This is to say that this is the description of the Property Type"

    name = fields.Char("Property Type", required=True)
