from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"

    name = fields.Char("Name", required=True)
