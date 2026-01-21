from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type Information'

    name = fields.Char(string='Property Type', required=True)
