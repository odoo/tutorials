from odoo import fields, models

class property_tags(models.Model):
    _name = "estate.property.tags"
    _description = "Model to modelize Tags of Properties"

    name = fields.Char(string="Name", required=True)