from odoo import fields, models


class Tag(models.Model):
    _name = "estate.property.tag"
    _description = "Propert tag"

    name = fields.Char(required=True)
