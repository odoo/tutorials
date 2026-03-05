from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Types"
    _order = "sequence,name"

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order Property. Lower number more priority.")
    property_ids = fields.One2many('estate.property', 'property_type_id', string='property')
