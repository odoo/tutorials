from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Define tags for properties"

    name = fields.Char(required=True)