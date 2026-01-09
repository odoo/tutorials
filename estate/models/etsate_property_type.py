from odoo import models, fields, api


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Define Type of property (House, Apartment, Penthouse, Castle…)'
    _order = 'sequence, name desc'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(default=10)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        "Property Type must be unique."
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
