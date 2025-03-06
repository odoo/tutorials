from odoo import fields, models

class estate_Property_Tag(models.Model):
    _name = "estate.property.tag"
    _description = "relevent tags"

    name = fields.Char(required=True)
