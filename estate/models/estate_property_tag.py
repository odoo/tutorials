from odoo import fields , models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model for property tags"

    name = fields.Char(required=True)
