from odoo import fields, models, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'estate property type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type')
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [('check_estate_property_type_unique', 'UNIQUE (name)', "The name must be unique.")]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
