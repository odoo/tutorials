from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Specific types of properties"

    name = fields.Char(string="Name", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete='restrict')

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property type already created')
    ]
