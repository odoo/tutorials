from odoo import fields, models


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag for properites"

    name = fields.Char(string="Tag name", required=True)
