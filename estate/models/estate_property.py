from odoo import fields , models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Property name ' , required = True , translate = True)
