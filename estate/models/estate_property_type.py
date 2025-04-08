from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Types'
    _order = 'name'
    _sql_constraints = [
        (
            'estate_property_type_name_unique',
            'UNIQUE(name)',
            'The property types must be unique.',
        )
    ]

    name = fields.Char('Type', required=True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(
        compute='_compute_offer_count', string='Offer Count', readonly=True, copy=False
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
