from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(required=True)