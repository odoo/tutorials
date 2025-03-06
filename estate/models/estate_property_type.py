from odoo import fields, models

class estate_Property_Type(models.Model):
    _name = "estate.property.type"
    _description = "relevent type"

    name = fields.Char(required=True)
