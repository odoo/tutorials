from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Model containing property tags"

    name = fields.Char(required=True)
