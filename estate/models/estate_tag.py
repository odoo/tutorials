from odoo import fields, models


class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "property tag"

    name = fields.Char(required=True)
