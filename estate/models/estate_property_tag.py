from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Different Tags for Property"

    name = fields.Char("Tag")
