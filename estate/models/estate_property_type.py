from odoo import fields, models

class TypeModel(models.Model):
    _name = "estate_property_type"
    _description = "estate property type"

    name = fields.Char('Property Types', required=True)
    