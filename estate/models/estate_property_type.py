
from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)

    property_ids = fields.One2many('estate_property', 'property_type_id', string='Properties')

    offer_ids = fields.One2many('estate_property_offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
