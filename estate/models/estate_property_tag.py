from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is the model for the estate property tag"

    name = fields.Char(string="Name")
