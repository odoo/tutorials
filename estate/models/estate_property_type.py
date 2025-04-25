from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Property type name must be unique')
    ]
    _order = 'sequence'
    
    sequence = fields.Integer('Sequence', default=10, help="Used to order property types. Lower is better.", required=True)
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
#     line_ids = fields.One2may('estate.property.type.ldine','model_id')

# class EstatePropertyTypeLine(models.Model):
#     _name = 'estate.property.type.line'
#     _description = 'Property Type Line'

#     model_id = fields.Many2one('estate.property.type')
#     title = fields.Char(string = 'Title')
#     expected_price = fields.Float(string="Expected Price")
#     status = fields.Float(string = 'Status')