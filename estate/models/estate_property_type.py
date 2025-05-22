from odoo import _, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [('unique_type_name', 'UNIQUE(name)', _('Type name should be unique.'))]
