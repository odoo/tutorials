from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "this is defind the tag of properties"

    name = fields.Char("estate_property", required=True)
