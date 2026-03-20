from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "The types available for properties/real estates"
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    offer_count = fields.Integer(string='Offers Count', compute='_compute_offer_count')
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')

    _check_name = models.Constraint('UNIQUE(name)', 'Property type name must be unique')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
