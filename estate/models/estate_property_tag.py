from odoo import fields, models


class Estate_Property_Tag(models.Model):
    _name = "estate.property.tag"

    _description = "Estate Property Type"

    name = fields.Char(required=True)
