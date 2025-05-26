from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')
    sequence = fields.Integer('Sequence', help='Used to order property types. Lower is better.')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [('unique_type_name', 'UNIQUE(name)', 'Type name should be unique.')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
