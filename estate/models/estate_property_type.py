from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = 'name'

    name = fields.Char('Type', required=True)
    description = fields.Text()
    property_type_line_ids = fields.One2many('estate.property.type.line', 'name')

    _unique_type = models.Constraint(
        'UNIQUE(name)',
        'Property type name exists'
    )

class EstatePropertyTypeLine(models.Model):
    _name = 'estate.property.type.line'
    _description = 'estate property view per type'

    name = fields.Many2one('estate.property.type')
    title = fields.Char()
    expected_price = fields.Char()
    state = fields.Char()
