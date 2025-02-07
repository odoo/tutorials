from odoo import fields,models

class EstatePropertytype(models.Model):
    _name = "estate.property.type"
    _description ="It defines the estate property type"

    name= fields.Char(required=True)
