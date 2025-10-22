from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tags"


    name = fields.Char(required=True)
