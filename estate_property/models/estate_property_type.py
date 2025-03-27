from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    sequence = fields.Integer('Sequence', default=1)

    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Property type name must be unique')]

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
