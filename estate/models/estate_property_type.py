from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Types'
    _order = 'name'

    name = fields.Char(string="Property Type", required=True)
    sequence = fields.Integer(string="sequence", default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name='property_type_id', string="Property Types")
