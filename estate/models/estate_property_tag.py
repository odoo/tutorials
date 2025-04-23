from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Property Tags"

    name = fields.Char("Name", required=True)
