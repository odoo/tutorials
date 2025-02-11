from odoo import fields, models

class EstatePropertyTag (models.Model):
    _name = "estate_property_tag_model"
    _description = "This is a property tag model"

    name = fields.Char(required=True)