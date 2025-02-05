from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is the model for estate property"


    name = fields.Char(string = "Name")
