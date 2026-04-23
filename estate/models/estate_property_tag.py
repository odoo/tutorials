from odoo import models, fields


class Estate_property_tag(models.Model):
    _name = "estate_property_tag"
    _description = "tag super mega trop bien"

    name = fields.Char(required=True)
