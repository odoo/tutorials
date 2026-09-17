from odoo import fields, models


class EstatePropertyTagModel(models.Model):
    _name = "estate_property_tag"
    _description = "The tag of an estate"

    name = fields.Char(required=True)
