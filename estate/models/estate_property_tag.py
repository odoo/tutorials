from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char('Tag Name', required=True, translate=True)

