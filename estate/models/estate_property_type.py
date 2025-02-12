from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "listing for property types"
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer("Sequence",default=1)
    offer_ids = fields.One2many(comodel_name='estate.property.offer',inverse_name='property_type_id',string='Offers')
    offer_count = fields.Integer(string='Offer Count',compute='_compute_offer_count')

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'A property type name must be unique')
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
