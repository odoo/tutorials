from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', inverse_name='property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    sequence = fields.Integer('Sequence', default=1, help='Used to order stages. Lower is better.')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_type_unique','UNIQUE(name)','The name must be unique'),
    ]
