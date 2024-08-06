from odoo import models, fields


class estate_property_tag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tag"
    name = fields.Char(required=True)
