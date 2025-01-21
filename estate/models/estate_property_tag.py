from odoo import fields, models

class TagModel(models.Model):
    _name = "estate_property_tag"
    _description = "estate property tag"

    name = fields.Char('Property Tags', required=True)
    