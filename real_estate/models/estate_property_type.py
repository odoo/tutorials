from odoo import fields, models

class EstatePropertyType(models.Model):

    _name = 'estate.property.type'
    _description = "Detail About Particular Property"

    name = fields.Char(
        string="Name",
        required=True
    )
