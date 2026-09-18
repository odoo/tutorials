from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Define the Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer(string='Sequence', default=1)
#   Offers handling
    offer_ids = fields.One2many('estate.property.offer','property_type_id','Property Type')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

#   Compute fields:

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            return True
        return True
