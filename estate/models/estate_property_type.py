from odoo import fields, models

class property_type(models.Model):
    _name = "estate.property.type"
    _description = "Model to modelize Type of Properties"

    name = fields.Char(string="Name", required=True)