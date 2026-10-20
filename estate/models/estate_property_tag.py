from odoo import fields, models


class PropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(string="Name", required=True)
