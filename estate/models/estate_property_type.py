from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type module'
    _order = 'name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    property_ids = fields.One2many('estate.property', 'estate_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)',
         'The property type must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
