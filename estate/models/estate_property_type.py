from odoo import fields, models


class estate_property_type(models.Model):
    _name='estate.property.type'
    _description="Real estate property types"
    _rec_name="name"

    name = fields.Char(required=True)
