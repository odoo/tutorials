from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'

    name = fields.Char('Property type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'The Property type should be unique')]
