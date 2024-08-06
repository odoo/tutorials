from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'It describes how property is i.e renovated, cozy'

    name = fields.Char(required=True)
