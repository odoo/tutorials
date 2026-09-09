from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this model is used to define tags to the properties"

    name = fields.Char(string="Tags")
