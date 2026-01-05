from odoo import models, fields


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Define Type of property (House, Apartment, Penthouse, Castle…)'

    name = fields.Char(required=True)
