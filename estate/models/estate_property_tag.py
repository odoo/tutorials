from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string='Name', required=True)
