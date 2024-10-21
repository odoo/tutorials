from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type modelisation'
    _order = 'sequence asc, name asc'
    _sql_constraints = [('unique_name', 'unique(name)', 'Type name must be unique')]

    name = fields.Char(required=True, string='Name')
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer(default=1)

    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute='_compute_offer_count', string='Offer Count')

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
