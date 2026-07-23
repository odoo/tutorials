from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "A list of tags that categorize the properities"

    name = fields.Char(string="Name", required=True)
