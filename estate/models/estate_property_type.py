from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ici je mets une phrase 2"

    name = fields.Char(required=True)
