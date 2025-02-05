from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description =  "Property Types"

    name = fields.Char(string="Name", required=True)
    