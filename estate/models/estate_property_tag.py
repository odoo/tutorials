from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = 'Estate Property Tag'

    name = fields.Char(
        string='Name',
        required=True,
        default="Unknown",
    )
