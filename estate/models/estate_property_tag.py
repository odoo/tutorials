from odoo import models, fields

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Tag for the estates_property model (Many2Many)"

    name = fields.Char(required=True)
