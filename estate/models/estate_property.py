from odoo import models, fields

class estate_property(models.Model):

    _name = "estate.property"
    _description = "Damn this model is good for doing real estate related stuff"

    name = fields.Char(required=True)