from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tag of properties"

    #Adding fields
    name = fields.Char(required=True)